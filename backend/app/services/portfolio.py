"""
Portfolio Service - CRUD operations dla portfolio
"""
from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.portfolio import PortfolioItem
from app.schemas.portfolio import PortfolioItemCreate, PortfolioItemUpdate


class PortfolioService:
    """
    Serwis do zarzadzania portfolio uzytkownika.
    """

    @staticmethod
    def get_all(db: Session, user_id: int) -> List[PortfolioItem]:
        """
        Pobierz wszystkie pozycje portfolio dla uzytkownika.
        """
        return db.query(PortfolioItem).filter(PortfolioItem.user_id == user_id).all()

    @staticmethod
    def get_by_id(db: Session, item_id: int, user_id: int) -> Optional[PortfolioItem]:
        """
        Pobierz pojedyncza pozycje portfolio po ID.
        """
        return db.query(PortfolioItem).filter(
            PortfolioItem.id == item_id,
            PortfolioItem.user_id == user_id
        ).first()

    @staticmethod
    def create(db: Session, user_id: int, item: PortfolioItemCreate) -> PortfolioItem:
        """
        Dodaj nowa pozycje do portfolio.
        """
        db_item = PortfolioItem(
            user_id=user_id,
            symbol=item.symbol.upper(),  # Zawsze uppercase (AAPL, nie aapl)
            entry_price=item.entry_price,
            quantity=item.quantity,
            notes=item.notes
        )
        db.add(db_item)
        db.commit()
        db.refresh(db_item)
        return db_item

    @staticmethod
    def update(
        db: Session,
        item_id: int,
        user_id: int,
        updates: PortfolioItemUpdate
    ) -> Optional[PortfolioItem]:
        """
        Edytuj istniejaca pozycje portfolio.
        """
        db_item = PortfolioService.get_by_id(db, item_id, user_id)
        if not db_item:
            return None

        # Update tylko podanych pol (partial update)
        if updates.entry_price is not None:
            db_item.entry_price = updates.entry_price
        if updates.quantity is not None:
            db_item.quantity = updates.quantity
        if updates.notes is not None:
            db_item.notes = updates.notes

        db.commit()
        db.refresh(db_item)
        return db_item

    @staticmethod
    def delete(db: Session, item_id: int, user_id: int) -> bool:
        """
        Usun pozycje z portfolio.

        Returns:
            True jesli usunieto, False jesli nie znaleziono
        """
        db_item = PortfolioService.get_by_id(db, item_id, user_id)
        if not db_item:
            return False

        db.delete(db_item)
        db.commit()
        return True
