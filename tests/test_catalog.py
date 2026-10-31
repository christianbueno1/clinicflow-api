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
