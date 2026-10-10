"""Which peoples have animation packs, the models (looks) each pack must fit, and the tags clips may use."""
MOD_ID = "endexpansion"
MIN_CLIPS = 50
GEOMETRY_DIRS = ["src/client/resources/assets/endexpansion/geometry"]

SPECIES = {
    "shulkin": {"name": "Shulkin", "looks": ["shulkin", "shulkin_child"]},
    "chorrin": {"name": "Chorrin", "looks": ["chorrin", "chorrin_child"]},
    # the Endarchs have no children (the Court's secret)
    "endarch": {"name": "Endarchs", "looks": ["endarch_lord", "endarch_marshal", "endarch_riftguard"], "children": False},
}

JOBS = {
    "shulkin": ["archivist", "lamplighter", "weaver", "shellwright", "wayfinder", "keeper", "hallkeeper", "trader"],
    "chorrin": ["grove_tender", "kiln_keeper", "stonecutter", "cook", "blinker", "brewer", "herder", "gatherer", "hallkeeper", "trader"],
    "endarch": ["lord", "marshal", "riftguard", "herald", "seer", "steward"],
}
MANNERS = ["steady", "shy", "restless", "busy", "flighty", "proud"]

# adult/child: age; social: a chat partner is near; talking: in a conversation with the player;
# job:<job>: their job (children have none); manner:<manner>: how they behave while you talk (their personality);
# working: at their workplace in working hours; rank:<rank>: which Endarch body (lord, marshal, riftguard), while
# job:<role> is their role at Court (a Herald, Seer or Steward has a lord's or marshal's body)
TAGS = {
    "common": {"adult", "child", "social", "talking", "working"} | {"manner:" + m for m in MANNERS},
    "endarch": {"rank:lord", "rank:marshal", "rank:riftguard"},
}
for _s, _jobs in JOBS.items():
    TAGS[_s] = set(TAGS.get(_s, ())) | {"job:" + j for j in _jobs}
