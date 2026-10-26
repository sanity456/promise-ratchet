import json


CONTEXT = "Free appliance inspection service for booked community members."
INITIAL = "The service will inspect every booked appliance without charging the member."
STRONGER = "The service will inspect every booked appliance without charging the member and will return each appliance without a delivery fee."
WEAKER = "The service will inspect some booked appliances without charging the member."
PROMPT = "Compare two public service commitments under one fixed context"
YES = {"new_entails_old": "YES", "old_entails_new": "NO", "same_scope": "YES"}
NO = {"new_entails_old": "NO", "old_entails_new": "YES", "same_scope": "YES"}


def setup(ratchet, direct_vm, direct_alice):
    direct_vm.sender = direct_alice
    ratchet.open_promise("repairs", CONTEXT, INITIAL)


def judgment(direct_vm, verdict):
    direct_vm.mock_llm(r".*" + PROMPT + r".*", json.dumps(verdict))


def test_stronger_promise_ratchets_and_preserves_history(ratchet, direct_vm, direct_alice):
    setup(ratchet, direct_vm, direct_alice)
    root = ratchet.get_revision(direct_alice, "repairs", 0)
    judgment(direct_vm, YES)
    revision_hash = ratchet.tighten_promise("repairs", 0, STRONGER)
    state = ratchet.get_promise(direct_alice, "repairs")
    assert state["version"] == 1
    assert state["current_hash"] == revision_hash
    assert state["current_promise"] == STRONGER
    assert ratchet.get_revision(direct_alice, "repairs", 0) == root
    revision = ratchet.get_revision(direct_alice, "repairs", 1)
    assert revision["previous_hash"] == root["hash"]
    assert revision["judgment"] == YES
    assert direct_vm.run_validator() is True


def test_weaker_or_unclear_proposal_cannot_advance(ratchet, direct_vm, direct_alice):
    setup(ratchet, direct_vm, direct_alice)
    original = ratchet.get_promise(direct_alice, "repairs")
    for verdict in (NO, {"new_entails_old": "UNCLEAR", "old_entails_new": "UNCLEAR", "same_scope": "YES"}):
        judgment(direct_vm, verdict)
        with direct_vm.expect_revert("not_strictly_stronger"):
            ratchet.tighten_promise("repairs", 0, WEAKER)
    assert ratchet.get_promise(direct_alice, "repairs") == original
    assert ratchet.get_revision(direct_alice, "repairs", 1) == {}


def test_stale_version_and_unauthorized_caller_fail(ratchet, direct_vm, direct_alice, direct_bob):
    setup(ratchet, direct_vm, direct_alice)
    direct_vm.sender = direct_bob
    with direct_vm.expect_revert("promise_missing"):
        ratchet.tighten_promise("repairs", 0, STRONGER)
    direct_vm.sender = direct_alice
    with direct_vm.expect_revert("stale_version"):
        ratchet.tighten_promise("repairs", 1, STRONGER)
    with direct_vm.expect_revert("unchanged_promise"):
        ratchet.tighten_promise("repairs", 0, INITIAL)


def test_seal_makes_commitment_final(ratchet, direct_vm, direct_alice):
    setup(ratchet, direct_vm, direct_alice)
    final_hash = ratchet.seal_promise("repairs", 0)
    assert ratchet.get_promise(direct_alice, "repairs")["sealed"] is True
    assert ratchet.get_promise(direct_alice, "repairs")["current_hash"] == final_hash
    with direct_vm.expect_revert("promise_sealed"):
        ratchet.tighten_promise("repairs", 0, STRONGER)


def test_validator_checks_every_consensus_field(ratchet, direct_vm, direct_alice):
    setup(ratchet, direct_vm, direct_alice)
    judgment(direct_vm, YES)
    ratchet.tighten_promise("repairs", 0, STRONGER)
    forged = {"new_entails_old": "YES", "old_entails_new": "NO", "same_scope": "NO"}
    assert direct_vm.run_validator(leader_result=forged) is False
    forged_extra = dict(YES, hidden="unverified")
    assert direct_vm.run_validator(leader_result=forged_extra) is False


def test_malformed_model_response_cannot_change_state(ratchet, direct_vm, direct_alice):
    setup(ratchet, direct_vm, direct_alice)
    judgment(direct_vm, {"new_entails_old": "YES"})
    with direct_vm.expect_revert("invalid_model_shape"):
        ratchet.tighten_promise("repairs", 0, STRONGER)
    assert ratchet.get_promise(direct_alice, "repairs")["version"] == 0
