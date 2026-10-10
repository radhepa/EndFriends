package dev.endexpansion.client.render;

import dev.endexpansion.client.anim.Pose;
import net.minecraft.client.renderer.block.BlockModelRenderState;
import net.minecraft.client.renderer.entity.state.LivingEntityRenderState;

/** Render state for every mob in the mod; each renderer fills the fields its model uses. */
public class EndRenderState extends LivingEntityRenderState {
    /** People: in a conversation, asleep, at work, lid shut (Shulkin), hauling a block (thrall), fighting. */
    public boolean talking, sleeping, working, closed, carrying, aggressive;
    /** 0..1 progress of a melee swing. */
    public float swing;
    /** Creatures: in flight (Driftray), sitting (Voidhound), the grove grown back 0..1 (Groveback). */
    public boolean flying, sitting;
    public float grove = 1.0F;
    /** The block a thrall carries. */
    public final BlockModelRenderState carriedBlock = new BlockModelRenderState();
    /** People: the clips they're acting out this frame (tools/animations). */
    public final Pose pose = new Pose();
}
