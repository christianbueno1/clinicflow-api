import math

import pytest


async def test_specialty_duplicate_and_delete_with_doctors(
    client, make_specialty, make_doctor
):
    s = await make_specialty("Neurología")
    dup = await client.post("/specialties", json={"name": "Neurología"})
    assert dup.status_code == 409

    await make_doctor(specialty_id=s["id"])
    blocked = await client.delete(f"/specialties/{s['id']}")
    assert blocked.status_code == 409


async def test_doctor_validations(client, make_doctor, make_specialty):
    s = await make_specialty()
    d = await make_doctor()

    bad_cedula = await client.post(
        "/doctors",
        json={
            "first_name": "Lawrence",
            "last_name": "Kutner",
            "identification_number": "1234567890",
            "license_number": "X-1",
            "specialty_id": s["id"],
        },
    )
    assert bad_cedula.status_code == 422

    dup_license = await client.post(
        "/doctors",
        json={
            "first_name": "Chris",
            "last_name": "Taub",
            "identification_number": "1104680135",
            "license_number": d["license_number"],
            "specialty_id": s["id"],
        },
    )
    assert dup_license.status_code == 409


async def test_doctor_soft_delete(client, make_doctor):
    d = await make_doctor()
    assert (await client.delete(f"/doctors/{d['id']}")).status_code == 204
    assert (await client.get(f"/doctors/{d['id']}")).status_code == 404


async def test_patient_email_is_normalized_and_unique(client, make_patient):
    p = await make_patient(email="Giant@Example.com")
    assert p["email"] == "giant@example.com"

    r = await client.post(
        "/patients",
        json={
            "first_name": "X",
            "last_name": "Y",
            "date_of_birth": "1970-01-01",
            "sex": "male",
            "phone": "0991234567",
            "identification_number": "1710034065",
            "email": "GIANT@example.com",
        },
    )
    assert r.status_code == 409


async def test_patient_patch_null_semantics(client, make_patient):
    p = await make_patient(address="Av. Amazonas", email="a@example.com")

    r = await client.patch(
        f"/patients/{p['id']}", json={"address": None, "email": None}
    )
    assert r.json()["address"] is None
    assert r.json()["email"] is None

    r = await client.patch(f"/patients/{p['id']}", json={"first_name": None})
    assert r.status_code == 200
    assert r.json()["first_name"] == "Stacy"  # null ignorado en campos obligatorios


async def test_patient_422_reports_all_errors(client):
    r = await client.post(
        "/patients",
        json={
            "first_name": "X",
            "last_name": "Y",
            "date_of_birth": "2099-01-01",
            "sex": "other",
            "phone": "abc",
            "identification_number": "1234567890",
            "email": "no-es-email",
        },
    )
    assert r.status_code == 422
    assert len(r.json()["detail"]) == 5


async def _doctors_25(make_specialty, make_doctor):
    uro = await make_specialty("Urología")
    otra = await make_specialty("Otra")
    for i in range(3):
        await make_doctor(f"Uro{i}", specialty_id=uro["id"])
    await make_doctor("UroX", specialty_id=uro["id"], is_active=False)
    for i in range(21):
        await make_doctor(f"Gen{i:02d}", specialty_id=otra["id"])
    return uro, otra


async def test_doctors_page_totals(client, make_specialty, make_doctor):
    await _doctors_25(make_specialty, make_doctor)
    body = (await client.get("/doctors", params={"page": 1, "page_size": 20})).json()
    assert len(body["items"]) == 20
    assert (body["total"], body["page"], body["page_size"], body["total_pages"]) == (
        25,
        1,
        20,
        2,
    )

    last = (await client.get("/doctors", params={"page": 3, "page_size": 10})).json()
    assert len(last["items"]) == 5
    assert (last["total"], last["total_pages"]) == (25, 3)


async def test_doctors_pages_have_no_duplicates_or_gaps(
    client, make_specialty, make_doctor
):
    await _doctors_25(make_specialty, make_doctor)
    ids = []
    for page in (1, 2, 3):
        r = await client.get("/doctors", params={"page": page, "page_size": 10})
        ids += [d["id"] for d in r.json()["items"]]
    assert len(ids) == 25 and len(set(ids)) == 25


async def test_doctors_filter_by_specialty_and_active(
    client, make_specialty, make_doctor
):
    uro, _ = await _doctors_25(make_specialty, make_doctor)
    base = {"page": 1, "page_size": 20, "specialty_id": uro["id"]}

    r = (await client.get("/doctors", params=base)).json()
    assert (len(r["items"]), r["total"], r["total_pages"]) == (4, 4, 1)

    r = (await client.get("/doctors", params={**base, "is_active": True})).json()
    assert (len(r["items"]), r["total"]) == (3, 3)

    r = (await client.get("/doctors", params={**base, "is_active": False})).json()
    assert r["total"] == 1

    # filtro + segunda página (fuera de rango): items vacío, total real
    r = (await client.get("/doctors", params={**base, "page": 2})).json()
    assert r["items"] == [] and r["total"] == 4


async def test_doctors_total_multiple_of_page_size(client, make_specialty, make_doctor):
    uro, _ = await _doctors_25(make_specialty, make_doctor)
    r = (
        await client.get("/doctors", params={"specialty_id": uro["id"], "page_size": 2})
    ).json()
    assert (r["total"], r["total_pages"]) == (4, math.ceil(4 / 2))


async def test_doctors_empty_filter_and_unknown_specialty(
    client, make_specialty, make_doctor
):
    await _doctors_25(make_specialty, make_doctor)
    vacia = await make_specialty("Sin doctores")
    for sid in (vacia["id"], "3fa85f64-5717-4562-b3fc-2c963f66afa6"):
        r = await client.get("/doctors", params={"specialty_id": sid})
        assert r.status_code == 200
        assert r.json()["items"] == []
        assert (r.json()["total"], r.json()["total_pages"]) == (0, 0)


async def test_doctors_soft_deleted_never_count(client, make_specialty, make_doctor):
    await _doctors_25(make_specialty, make_doctor)
    victim = (await client.get("/doctors", params={"is_active": False})).json()[
        "items"
    ][0]
    assert (await client.delete(f"/doctors/{victim['id']}")).status_code == 204
    for params in ({}, {"is_active": False}, {"is_active": True}):
        r = (await client.get("/doctors", params={**params, "page_size": 100})).json()
        assert victim["id"] not in [d["id"] for d in r["items"]]
    assert (await client.get("/doctors")).json()["total"] == 24


@pytest.mark.parametrize(
    "params",
    [
        {"page": 0},
        {"page": -1},
        {"page_size": 0},
        {"page_size": 101},
        {"specialty_id": "no-es-uuid"},
    ],
)
async def test_doctors_list_validation(client, params):
    assert (await client.get("/doctors", params=params)).status_code == 422


async def test_patients_page_and_search(client, make_patient):
    for i in range(12):
        await make_patient(f"Apellido{i:02d}")
    await make_patient("Distinto", first_name="Zola")

    r = (await client.get("/patients", params={"page": 2, "page_size": 5})).json()
    assert (len(r["items"]), r["total"], r["total_pages"]) == (5, 13, 3)

    r = (await client.get("/patients", params={"q": "zola"})).json()
    assert (r["total"], r["total_pages"]) == (1, 1)

    r = (await client.get("/patients", params={"q": "nadie-con-este-nombre"})).json()
    assert (r["items"], r["total"], r["total_pages"]) == ([], 0, 0)


async def test_patients_soft_deleted_do_not_count(client, make_patient):
    p = await make_patient()
    await make_patient("Otro")
    await client.delete(f"/patients/{p['id']}")
    assert (await client.get("/patients")).json()["total"] == 1
