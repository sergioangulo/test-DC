from app.domain.message_builder import MessageContext, build_messages, validate_message


def test_builds_and_validates_base_case_messages_with_policy_ref():
    ctx = MessageContext(
        decision_state="PENDIENTE_APROBACION",
        affected_flight="LA500",
        delay_minutes=160,
        new_departure="17:10",
        gate="24",
        gate_time="2026-09-15T10:55:00Z",
        missed_connection=True,
        policy_version="POL-DELAY-2026-03",
        proposed_option={"option_id": "O1", "flight_number": "LA2412", "date": "2026-09-16", "departure": "08:15"},
        overnight_required=True,
        minor_approval_rule_id="R5",
        blocking_reasons=[],
        no_option_reason=None,
    )
    bundle = build_messages(ctx)
    assert bundle.messages_blocked == 0
    assert any(m["policy_ref"] == "POL-DELAY-2026-03" for m in bundle.messages)
    assert any("Si prefieres no viajar" in m["text"] for m in bundle.messages)

    invalid_msg = {"text": "Te ofrecemos cambio sin costo", "kind": "NEXT_STEP", "policy_ref": None, "evidence_refs": ["R3"]}
    assert validate_message(invalid_msg, "POL-DELAY-2026-03") is False


def _proposal_ctx(fare: int, currency: str | None) -> MessageContext:
    opt = {"option_id": "O1", "flight_number": "LA2412", "date": "2026-09-16", "departure": "08:15",
           "fare_difference": fare, "currency": currency}
    return MessageContext("AUTOMATICA", "LA500", 160, "17:10", None, None, True,
                          "POL-DELAY-2026-03", opt, False, None, [], None)


def test_proposal_text_reflects_real_fare_difference():
    free_text = _proposal_text_of(_proposal_ctx(0, "CLP"))
    assert "sin costo adicional" in free_text

    fee_text = _proposal_text_of(_proposal_ctx(45000, "CLP"))
    assert "45000" in fee_text and "CLP" in fee_text
    assert "sin costo" not in fee_text


def _proposal_text_of(ctx: MessageContext) -> str:
    proposal = next(m for m in build_messages(ctx).messages if m["message_id"] == "MSG_PROPOSAL")
    return proposal["text"]
