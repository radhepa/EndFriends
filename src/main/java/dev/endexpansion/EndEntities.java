package dev.endexpansion;

import dev.endexpansion.entity.Chorrin;
import dev.endexpansion.entity.Driftray;
import dev.endexpansion.entity.Endarch;
import dev.endexpansion.entity.EndermanThrall;
import dev.endexpansion.entity.Groveback;
import dev.endexpansion.entity.Resident;
import dev.endexpansion.entity.Shulkin;
import dev.endexpansion.entity.Voidhound;
import dev.endexpansion.registry.MobEntry;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.MobCategory;
import net.minecraft.world.level.biome.Biomes;

/**
 * Every mob in the mod: hitbox (sized to the model), attributes, and where the wild ones spawn.
 * Villagers and the Court come from their villages (and spawn eggs); Grovebacks and Driftrays also
 * live wild on the outer islands. The client registers a model and renderer for each.
 */
public final class EndEntities {
    private EndEntities() {}

    // -- the Shulkin and the Chorrin -------------------------------------------------------------
    public static final EntityType<Shulkin> SHULKIN = MobEntry.<Shulkin>builder("shulkin", (t, l) -> new Shulkin(t, l, false), MobCategory.MISC)
            .size(0.8F, 2.6F, 2.25F).attributes(() -> Resident.residentAttributes(30.0)).register();
    public static final EntityType<Shulkin> SHULKIN_CHILD = MobEntry.<Shulkin>builder("shulkin_child", (t, l) -> new Shulkin(t, l, true), MobCategory.MISC)
            .size(0.5F, 1.25F, 1.0F).attributes(() -> Resident.residentAttributes(14.0)).register();
    public static final EntityType<Chorrin> CHORRIN = MobEntry.<Chorrin>builder("chorrin", (t, l) -> new Chorrin(t, l, false), MobCategory.MISC)
            .size(0.9F, 1.9F, 1.45F).attributes(() -> Resident.residentAttributes(26.0).add(net.minecraft.world.entity.ai.attributes.Attributes.ARMOR, 4.0)).register();
    public static final EntityType<Chorrin> CHORRIN_CHILD = MobEntry.<Chorrin>builder("chorrin_child", (t, l) -> new Chorrin(t, l, true), MobCategory.MISC)
            .size(0.55F, 1.1F, 0.8F).attributes(() -> Resident.residentAttributes(12.0)).register();

    // -- the Court ---------------------------------------------------------------------------------
    public static final EntityType<Endarch> ENDARCH_LORD = MobEntry.<Endarch>builder("endarch_lord", (t, l) -> new Endarch(t, l, Endarch.Rank.LORD), MobCategory.MISC)
            .size(0.9F, 3.8F, 3.4F).attributes(() -> Endarch.attributes(Endarch.Rank.LORD)).register();
    public static final EntityType<Endarch> ENDARCH_MARSHAL = MobEntry.<Endarch>builder("endarch_marshal", (t, l) -> new Endarch(t, l, Endarch.Rank.MARSHAL), MobCategory.MISC)
            .size(0.9F, 3.5F, 3.1F).attributes(() -> Endarch.attributes(Endarch.Rank.MARSHAL)).register();
    public static final EntityType<Endarch> ENDARCH_RIFTGUARD = MobEntry.<Endarch>builder("endarch_riftguard", (t, l) -> new Endarch(t, l, Endarch.Rank.RIFTGUARD), MobCategory.MISC)
            .size(0.8F, 3.4F, 3.0F).attributes(() -> Endarch.attributes(Endarch.Rank.RIFTGUARD)).register();
    public static final EntityType<EndermanThrall> ENDERMAN_THRALL = MobEntry.builder("enderman_thrall", EndermanThrall::new, MobCategory.MISC)
            .size(0.6F, 2.9F, 2.55F).attributes(EndermanThrall::attributes).register();

    // -- creatures ---------------------------------------------------------------------------------
    public static final EntityType<Groveback> GROVEBACK = MobEntry.builder("groveback", Groveback::new, MobCategory.CREATURE)
            .size(1.4F, 1.4F, 1.1F).attributes(Groveback::attributes)
            .spawnRule(Groveback::checkSpawnRules)
            .spawnsIn(8, 2, 4, Biomes.END_HIGHLANDS, Biomes.END_MIDLANDS)
            .register();
    public static final EntityType<Driftray> DRIFTRAY = MobEntry.builder("driftray", Driftray::new, MobCategory.CREATURE)
            .size(1.6F, 1.1F, 0.8F).type(t -> t.passengerAttachments(1.05F)).attributes(Driftray::attributes)
            .spawnRule(Driftray::checkSpawnRules)
            .spawnsIn(5, 1, 3, Biomes.END_HIGHLANDS)
            .register();
    public static final EntityType<Voidhound> VOIDHOUND = MobEntry.builder("voidhound", Voidhound::new, MobCategory.MISC)
            .size(0.8F, 1.1F, 0.9F).attributes(Voidhound::attributes).register();

    /** Loads the class (the fields above register everything). */
    public static void register() {}
}
