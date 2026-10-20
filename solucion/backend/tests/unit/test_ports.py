from app.domain.ports import (
    FixedClock,
    InMemoryDecisionStore,
    RebookingCommand,
)


def test_fixed_clock_and_decision_store_contract():
    clock = FixedClock("2026-09-15T11:02:35Z")
    assert clock.now_iso() == "2026-09-15T11:02:35Z"

    store = InMemoryDecisionStore()
    store.save_decision({"decision_id": "dec-1", "booking_id": "ABC123"})
    assert store.get_decision("dec-1")["booking_id"] == "ABC123"

    cmd = RebookingCommand("O1", "key-1", "ABC123", ("P1", "P2"))
    assert cmd.option_id == "O1"
