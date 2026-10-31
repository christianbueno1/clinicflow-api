import asyncio
from datetime import datetime, time, timedelta, timezone

from tests.conftest import future

ECU = timezone(timedelta(hours=-5))


async def test_create_calculates_ends_at(book, make_patient, make_doctor):
    start = future()
    r = await book(await make_patient(), await make_doctor(), start, minutes=45)
    assert r.status_code == 201
    body = r.json()
    assert body["status"] == "scheduled"
    ends = datetime.fromisoformat(body["ends_at"])
    assert ends - start == timedelta(minutes=45)


async def test_doctor_overlap_is_rejected(book, make_patient, make_doctor):
    doctor = await make_doctor()
    start = future()
    assert (await book(await make_patient(), doctor, start, 45)).status_code == 201
    r = await book(await make_patient(), doctor, start + timedelta(minutes=30))
    assert r.status_code == 409
    assert "doctor" in r.json()["detail"].lower()


async def test_patient_overlap_with_other_doctor_is_rejected(
    book, make_patient, make_doctor
):
    patient = await make_patient()
    start = future()
    assert (
        await book(patient, await make_doctor("Cuddy"), start, 45)
    ).status_code == 201
    r = await book(patient, await make_doctor("Foreman"), start + timedelta(minutes=15))
    assert r.status_code == 409
    assert "paciente" in r.json()["detail"].lower()


async def test_back_to_back_appointments_are_allowed(book, make_patient, make_doctor):
    doctor = await make_doctor()
    start = future()
    assert (await book(await make_patient(), doctor, start, 45)).status_code == 201
    r = await book(await make_patient(), doctor, start + timedelta(minutes=45))
    assert r.status_code == 201


async def test_inactive_doctor_is_rejected(client, book, make_patient, make_doctor):
    doctor = await make_doctor()
    await client.patch(f"/doctors/{doctor['id']}", json={"is_active": False})
    r = await book(await make_patient(), doctor, future())
    assert r.status_code == 409


async def test_past_and_naive_dates_are_rejected(client, make_patient, make_doctor):
    patient, doctor = await make_patient(), await make_doctor()
    base = {"patient_id": patient["id"], "doctor_id": doctor["id"]}
    past = await client.post(
        "/appointments", json={**base, "starts_at": "2020-01-01T09:00:00-05:00"}
    )
    naive = await client.post(
        "/appointments",
        json={**base, "starts_at": future().replace(tzinfo=None).isoformat()},
    )
    assert past.status_code == 422
    assert naive.status_code == 422


async def test_unknown_doctor_or_patient_returns_404(client, make_patient, make_doctor):
    ghost = "3fa85f64-5717-4562-b3fc-2c963f66afa6"
    patient, doctor = await make_patient(), await make_doctor()
    start = future().isoformat()
    r1 = await client.post(
        "/appointments",
        json={"patient_id": patient["id"], "doctor_id": ghost, "starts_at": start},
    )
    r2 = await client.post(
        "/appointments",
        json={"patient_id": ghost, "doctor_id": doctor["id"], "starts_at": start},
    )
    assert r1.status_code == 404
    assert r2.status_code == 404


async def test_reschedule(client, book, make_patient, make_doctor):
    doctor = await make_doctor()
    start = future()
    a = (await book(await make_patient(), doctor, start, 45)).json()
    await book(
        await make_patient(), doctor, start + timedelta(minutes=45)
    )  # bloquea 09:45

    ok = await client.patch(
        f"/appointments/{a['id']}",
        json={"starts_at": (start + timedelta(hours=3)).isoformat()},
    )
    assert ok.status_code == 200

    clash = await client.patch(
        f"/appointments/{a['id']}",
        json={"starts_at": (start + timedelta(minutes=50)).isoformat()},
    )
    assert clash.status_code == 409


async def test_cancel_frees_the_slot_and_final_states_are_locked(
    client, book, make_patient, make_doctor
):
    doctor = await make_doctor()
    start = future()
    a = (await book(await make_patient(), doctor, start)).json()

    r = await client.patch(
        f"/appointments/{a['id']}/status", json={"status": "cancelled"}
    )
    assert r.status_code == 200
    assert r.json()["status"] == "cancelled"

    # el hueco quedó libre
    assert (await book(await make_patient(), doctor, start)).status_code == 201

    # estado final: no admite más cambios ni reprogramación
    again = await client.patch(
        f"/appointments/{a['id']}/status", json={"status": "completed"}
    )
    assert again.status_code == 409
    move = await client.patch(
        f"/appointments/{a['id']}", json={"reason": "otro motivo"}
    )
    assert move.status_code == 409


async def test_list_filters(client, book, make_patient, make_doctor):
    doctor, patient = await make_doctor(), await make_patient()
    start = future()
    a = (await book(patient, doctor, start)).json()
    await book(await make_patient(), doctor, start + timedelta(hours=1))
    await client.patch(f"/appointments/{a['id']}/status", json={"status": "cancelled"})

    by_doctor = (
        await client.get("/appointments", params={"doctor_id": doctor["id"]})
    ).json()
    by_status = (
        await client.get(
            "/appointments", params={"doctor_id": doctor["id"], "status": "scheduled"}
        )
    ).json()
    by_patient = (
        await client.get("/appointments", params={"patient_id": patient["id"]})
    ).json()
    assert len(by_doctor) == 2
    assert len(by_status) == 1
    assert len(by_patient) == 1


async def test_cannot_delete_doctor_or_patient_with_future_appointments(
    client, book, make_patient, make_doctor
):
    doctor, patient = await make_doctor(), await make_patient()
    a = (await book(patient, doctor, future())).json()

    assert (await client.delete(f"/doctors/{doctor['id']}")).status_code == 409
    assert (await client.delete(f"/patients/{patient['id']}")).status_code == 409

    await client.patch(f"/appointments/{a['id']}/status", json={"status": "cancelled"})

    assert (await client.delete(f"/doctors/{doctor['id']}")).status_code == 204
    assert (await client.delete(f"/patients/{patient['id']}")).status_code == 204


async def test_availability_marks_booked_slots(client, book, make_patient, make_doctor):
    doctor = await make_doctor()
    day = (datetime.now(ECU) + timedelta(days=7)).date()
    start = datetime.combine(day, time(9, 0), tzinfo=ECU)
    await book(await make_patient(), doctor, start, 45)

    r = await client.get(
        f"/doctors/{doctor['id']}/availability", params={"date": day.isoformat()}
    )
    assert r.status_code == 200
    slots = {
        datetime.fromisoformat(s["starts_at"]): s["available"]
        for s in r.json()["slots"]
    }
    assert slots[start] is False
    assert (
        slots[start + timedelta(minutes=30)] is False
    )  # el 09:30 cae dentro de los 45 min
    assert slots[start + timedelta(minutes=60)] is True


async def test_availability_of_inactive_doctor_is_409(client, make_doctor):
    doctor = await make_doctor()
    await client.patch(f"/doctors/{doctor['id']}", json={"is_active": False})
    r = await client.get(
        f"/doctors/{doctor['id']}/availability", params={"date": "2030-01-01"}
    )
    assert r.status_code == 409


async def test_concurrent_bookings_only_one_wins(book, make_patient, make_doctor):
    doctor = await make_doctor()
    p1, p2 = await make_patient(), await make_patient()
    start = future()

    r1, r2 = await asyncio.gather(book(p1, doctor, start), book(p2, doctor, start))

    assert sorted([r1.status_code, r2.status_code]) == [201, 409]
