# app/routers/drug.py
import json
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.drug import DrugCreate, DrugUpdate, DrugOut
from app.models.drug import Drug
from app.models.user import User
from app.routers.auth import get_current_user  # lub inna nazwa
router = APIRouter()

@router.post("/", response_model=DrugOut, status_code=status.HTTP_201_CREATED)
def create_drug(
    drug_data: DrugCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Tworzy nowy lek przypisany do konkretnego usera (user_uuid).
    """
    # Jeśli chcesz mieć pewność, że user_uuid == current_user.uuid,
    # możesz sprawdzić i ewentualnie rzucić 403:
    if drug_data.user_uuid != current_user.uuid:
        raise HTTPException(status_code=403, detail="Cannot create drug for another user")

    # Zamieniamy listę times na JSON:
    times_json = drug_data.times.__str__()
    print(times_json)

    new_drug = Drug(
        user_uuid=drug_data.user_uuid,
        name=drug_data.name,
        dosage=drug_data.dosage,
        date_from=drug_data.date_from,
        date_to=drug_data.date_to,
        additional_info=drug_data.additional_info,
        times=times_json,
        is_notification_enabled=drug_data.is_notification_enabled
    )
    db.add(new_drug)
    db.commit()
    db.refresh(new_drug)

    return new_drug

@router.get("/", response_model=List[DrugOut])
def list_drugs(
    user_uuid: str = Query(..., description="UUID użytkownika"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Zwraca listę wszystkich leków dla danego user_uuid.
    """
    # Ewentualnie sprawdzamy, czy user_uuid == current_user.uuid
    if user_uuid != current_user.uuid:
        raise HTTPException(status_code=403, detail="Cannot list drugs for another user")

    drugs = db.query(Drug).filter(Drug.user_uuid == user_uuid).all()

    return drugs

@router.get("/{drug_id}", response_model=DrugOut)
def get_drug(
    drug_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Zwraca pojedynczy lek (po id).
    """
    drug = db.query(Drug).filter(Drug.id == drug_id).first()
    if not drug:
        raise HTTPException(status_code=404, detail="Drug not found")

    if drug.user_uuid != current_user.uuid:
        raise HTTPException(status_code=403, detail="Not your drug")

    return drug

@router.patch("/{drug_id}", response_model=DrugOut)
def update_drug(
    drug_id: str,
    drug_data: DrugUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Aktualizuje istniejący lek. Wszystkie pola w DrugUpdate są opcjonalne.
    """
    drug = db.query(Drug).filter(Drug.id == drug_id).first()
    if not drug:
        raise HTTPException(status_code=404, detail="Drug not found")
    if drug.user_uuid != current_user.uuid:
        raise HTTPException(status_code=403, detail="Not your drug")

    # Aktualizujemy tylko te pola, które są nie-None
    if drug_data.name is not None:
        drug.name = drug_data.name
    if drug_data.dosage is not None:
        drug.dosage = drug_data.dosage
    if drug_data.date_from is not None:
        drug.date_from = drug_data.date_from
    if drug_data.date_to is not None:
        drug.date_to = drug_data.date_to
    if drug_data.additional_info is not None:
        drug.additional_info = drug_data.additional_info
    if drug_data.times is not None:
        drug.times = json.dumps(drug_data.times)
    if drug_data.is_notification_enabled is not None:
        drug.is_notification_enabled = drug_data.is_notification_enabled

    db.commit()
    db.refresh(drug)
    return drug

@router.delete("/{drug_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_drug(
    drug_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Usuwa lek po id.
    """
    drug = db.query(Drug).filter(Drug.id == drug_id).first()
    if not drug:
        raise HTTPException(status_code=404, detail="Drug not found")
    if drug.user_uuid != current_user.uuid:
        raise HTTPException(status_code=403, detail="Not your drug")

    db.delete(drug)
    db.commit()
    return  # 204 No Content
