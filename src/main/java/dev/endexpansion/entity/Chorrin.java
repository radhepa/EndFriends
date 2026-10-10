package dev.endexpansion.entity;

import dev.endexpansion.talk.Manner;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.sounds.SoundEvent;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.util.RandomSource;
import net.minecraft.world.damagesource.DamageSource;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.level.Level;
import org.jspecify.annotations.Nullable;

/**
 * Grove-folk of the outer islands: heavy, stone-skinned, chorus-crowned and mouthless (they hum).
 * Startled, a Chorrin blinks a few blocks away as if it had eaten chorus fruit; sprouts do too, and
 * a flighty one blinks a short hop now and then even mid-conversation, and one who turns away from
 * you because they're upset with you blinks away. Each is named for their grove: "Mott of Low Grove".
 */
public class Chorrin extends Resident {
    private static final int BLINK_COOLDOWN = 60, BLINK_RANGE = 8;

    private final boolean child;
    private int blinkCooldown, hopTimer = 100;

    public Chorrin(EntityType<? extends Chorrin> type, Level level, boolean child) {
        super(type, level);
        this.child = child;
    }

    @Override public String people() { return "chorrin"; }
    @Override public boolean isChild() { return child; }
    @Override protected String defaultJob() { return child ? "" : "gatherer"; }

    @Override
    public String title() {
        if (child) return "Sprout";
        return switch (job) {
            case "grove_tender" -> "Grove-tender";
            case "kiln_keeper" -> "Kiln-keeper";
            case "stonecutter" -> "Stonecutter";
            case "cook" -> "Cook";
            case "blinker" -> "Blinker";
            case "brewer" -> "Brewer";
            case "herder" -> "Herder";
            case "hallkeeper" -> "Hallkeeper";
            case "trader" -> "Trader";
            default -> "Gatherer";
        };
    }

    @Override
    protected String fullName(String first, RandomSource random) {
        return first + " of " + settlement().name();
    }

    @Override
    public boolean hurtServer(ServerLevel level, DamageSource source, float damage) {
        boolean hurt = super.hurtServer(level, source, damage);
        if (hurt && isAlive() && blinkCooldown == 0) blink();
        return hurt;
    }

    /** Blinks a few blocks away, like chorus fruit. */
    public boolean blink() {
        for (int i = 0; i < 16; i++) {
            double x = getX() + (random.nextDouble() - 0.5) * 2 * BLINK_RANGE;
            double y = getY() + random.nextInt(5) - 1;
            double z = getZ() + (random.nextDouble() - 0.5) * 2 * BLINK_RANGE;
            if (blinkTo(x, y, z)) return true;
        }
        return false;
    }

    private boolean blinkTo(double x, double y, double z) {
        double fromX = getX(), fromY = getY(), fromZ = getZ();
        if (!randomTeleport(x, y, z, true, s -> false)) return false;
        getNavigation().stop();
        level().playSound(null, fromX, fromY, fromZ, SoundEvents.CHORUS_FRUIT_TELEPORT, getSoundSource(), 1.0F, child ? 1.4F : 1.0F);
        playSound(SoundEvents.CHORUS_FRUIT_TELEPORT, 1.0F, child ? 1.4F : 1.0F);
        blinkCooldown = BLINK_COOLDOWN;
        return true;
    }

    /** Flighty: now and then a short hop to somewhere else near the player, and on with the conversation. */
    @Override
    protected void talkStep(ServerPlayer partner) {
        if (manner() != Manner.FLIGHTY) {
            super.talkStep(partner);
            return;
        }
        if (!getNavigation().isDone()) getNavigation().stop();
        if (--hopTimer > 0) return;
        hopTimer = 160 + random.nextInt(200);
        for (int i = 0; i < 12; i++) {
            double x = getX() + (random.nextDouble() - 0.5) * 6, z = getZ() + (random.nextDouble() - 0.5) * 6;
            double d = partner.distanceToSqr(x, getY(), z);
            if (d >= 4 && d <= 25 && blinkTo(x, getY() + random.nextInt(3) - 1, z)) return;
        }
    }

    @Override
    protected void leaveWith(ServerPlayer partner, String reason) {
        if (reason.equals("dislike")) blink();
        super.leaveWith(partner, reason);
    }

    @Override
    protected void customServerAiStep(ServerLevel level) {
        super.customServerAiStep(level);
        if (blinkCooldown > 0) blinkCooldown--;
    }

    /** A low hum (no mouth to say anything else with). */
    @Override protected @Nullable SoundEvent getAmbientSound() { return isSleeping() ? null : SoundEvents.NOTE_BLOCK_DIDGERIDOO.value(); }
    @Override protected SoundEvent getHurtSound(DamageSource source) { return SoundEvents.STONE_HIT; }
    @Override protected SoundEvent getDeathSound() { return SoundEvents.CHORUS_FLOWER_DEATH; }
    @Override public float getVoicePitch() { return (child ? 0.95F : 0.55F) + random.nextFloat() * 0.1F; }
    @Override protected float getSoundVolume() { return 0.5F; }
    @Override public int getAmbientSoundInterval() { return 320; }
}
