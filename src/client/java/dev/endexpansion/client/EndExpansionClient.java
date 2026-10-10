package dev.endexpansion.client;

import dev.endexpansion.EndEntities;
import dev.endexpansion.anim.Cue;
import dev.endexpansion.client.anim.Life;
import net.fabricmc.fabric.api.client.event.lifecycle.v1.ClientTickEvents;
import net.minecraft.client.Minecraft;
import net.minecraft.world.entity.LivingEntity;
import dev.endexpansion.client.model.DriftrayModel;
import dev.endexpansion.client.model.FolkModel;
import dev.endexpansion.client.model.Geometry;
import dev.endexpansion.client.model.GrovebackModel;
import dev.endexpansion.client.model.VoidhoundModel;
import dev.endexpansion.client.render.EndRenderState;
import dev.endexpansion.client.render.EndRenderer;
import dev.endexpansion.client.screen.ConversationScreen;
import dev.endexpansion.entity.EndFolk;
import dev.endexpansion.entity.EndermanThrall;
import dev.endexpansion.registry.MobEntry;
import dev.endexpansion.registry.MobRegistry;
import dev.endexpansion.talk.TalkPayload;
import java.util.List;
import net.fabricmc.api.ClientModInitializer;
import net.fabricmc.fabric.api.client.networking.v1.ClientPlayNetworking;
import net.fabricmc.fabric.api.client.rendering.v1.EntityRendererRegistry;
import net.fabricmc.fabric.api.client.rendering.v1.ModelLayerRegistry;
import net.minecraft.client.renderer.entity.EndermanRenderer;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.level.block.Blocks;

/**
 * Client wiring: a model layer per geometry file, a renderer per mob, and the conversation screen
 * opening (or updating) whenever the server sends a {@link TalkPayload}.
 */
public final class EndExpansionClient implements ClientModInitializer {
    /** Geometry files that aren't a mob of their own. */
    private static final List<String> EXTRA_MODELS = List.of("voidhound_pup");

    @Override
    public void onInitializeClient() {
        for (MobEntry<?> e : MobRegistry.all()) ModelLayerRegistry.registerModelLayer(Geometry.layer(e.id), () -> Geometry.load(e.id));
        for (String id : EXTRA_MODELS) ModelLayerRegistry.registerModelLayer(Geometry.layer(id), () -> Geometry.load(id));

        folk(EndEntities.SHULKIN, "shulkin", 0.5F);
        folk(EndEntities.SHULKIN_CHILD, "shulkin_child", 0.3F);
        folk(EndEntities.CHORRIN, "chorrin", 0.6F);
        folk(EndEntities.CHORRIN_CHILD, "chorrin_child", 0.35F);
        folk(EndEntities.ENDARCH_LORD, "endarch_lord", 0.7F);
        folk(EndEntities.ENDARCH_MARSHAL, "endarch_marshal", 0.7F);
        folk(EndEntities.ENDARCH_RIFTGUARD, "endarch_riftguard", 0.6F);
        EntityRendererRegistry.register(EndEntities.ENDERMAN_THRALL, ctx -> {
            var blocks = ctx.getBlockModelResolver();
            return new EndRenderer<EndermanThrall>(ctx, "enderman_thrall", FolkModel::new, 0.5F, (e, s) -> {
                pose(e, s);
                if (s.carrying) blocks.update(s.carriedBlock, Blocks.OBSIDIAN.defaultBlockState(), EndermanRenderer.BLOCK_DISPLAY_CONTEXT);
                else s.carriedBlock.clear();
            }).carrying();
        });
        EntityRendererRegistry.register(EndEntities.GROVEBACK, ctx -> new EndRenderer<>(ctx, "groveback", (root, id) -> new GrovebackModel(root), 0.9F,
                (e, s) -> s.grove = e.grove()));
        EntityRendererRegistry.register(EndEntities.DRIFTRAY, ctx -> new EndRenderer<>(ctx, "driftray", (root, id) -> new DriftrayModel(root), 0.8F,
                (e, s) -> s.flying = e.isFlying()));
        EntityRendererRegistry.register(EndEntities.VOIDHOUND, ctx -> new EndRenderer<>(ctx, "voidhound", "voidhound_pup", VoidhoundModel::new, 0.5F,
                (e, s) -> s.sitting = e.isInSittingPose()));

        animations();
        ClientPlayNetworking.registerGlobalReceiver(TalkPayload.TYPE, (payload, context) -> {
            var client = context.client();
            if (client.gui.screen() instanceof ConversationScreen screen && screen.matches(payload)) screen.update(payload);
            else if (payload.opening() && client.player != null) client.gui.setScreen(new ConversationScreen(payload));
        });
    }

    /**
     * The peoples' animation packs (docs/ANIMATIONS.md): who plays them, when they can't (asleep, fighting, a
     * Shulkin shut in its shell), and the tags that pick clips (job, manner, rank, at work).
     */
    static void animations() {
        java.util.function.Predicate<LivingEntity> able = e -> e instanceof EndFolk f && !f.isAggressive() && !f.flag(EndFolk.CLOSED)
                && !f.flag(EndFolk.SLEEPING);
        Life.register(EndEntities.SHULKIN, new Life.Kind("shulkin", able, EndExpansionClient::tags, e -> false));
        Life.register(EndEntities.SHULKIN_CHILD, new Life.Kind("shulkin", able, EndExpansionClient::tags, e -> true));
        Life.register(EndEntities.CHORRIN, new Life.Kind("chorrin", able, EndExpansionClient::tags, e -> false));
        Life.register(EndEntities.CHORRIN_CHILD, new Life.Kind("chorrin", able, EndExpansionClient::tags, e -> true));
        Life.register(EndEntities.ENDARCH_LORD, new Life.Kind("endarch", able, (e, t) -> { tags(e, t); t.add("rank:lord"); }, e -> false));
        Life.register(EndEntities.ENDARCH_MARSHAL, new Life.Kind("endarch", able, (e, t) -> { tags(e, t); t.add("rank:marshal"); }, e -> false));
        Life.register(EndEntities.ENDARCH_RIFTGUARD, new Life.Kind("endarch", able, (e, t) -> { tags(e, t); t.add("rank:riftguard"); }, e -> false));
        // in a conversation: 2 while their line types out, 1 while you choose what to say
        Life.conversation = e -> Minecraft.getInstance().gui.screen() instanceof ConversationScreen c && c.data().entityId() == e.getId()
                ? (c.speaking() ? 2 : 1) : 0;
        ClientTickEvents.END_CLIENT_TICK.register(Life::tickAll);
        ClientPlayNetworking.registerGlobalReceiver(Cue.TYPE, (cue, context) -> Life.cue(cue.entityId(), cue.trigger()));
    }

    /** job:&lt;job&gt; and manner:&lt;manner&gt; from the synced motion string, and working while at their workplace. */
    static void tags(LivingEntity e, java.util.Set<String> tags) {
        if (!(e instanceof EndFolk f)) return;
        String[] motion = f.motion().split("[|]");
        if (motion.length > 0 && !motion[0].isEmpty()) tags.add("job:" + motion[0]);
        if (motion.length > 1 && !motion[1].isEmpty()) tags.add("manner:" + motion[1]);
        if (f.flag(EndFolk.WORKING)) tags.add("working");
    }

    private static <T extends EndFolk> void folk(EntityType<T> type, String id, float shadow) {
        EntityRendererRegistry.register(type, ctx -> new EndRenderer<T>(ctx, id, FolkModel::new, shadow, EndExpansionClient::pose));
    }

    private static void pose(EndFolk e, EndRenderState s) {
        s.talking = e.flag(EndFolk.TALKING);
        s.sleeping = e.flag(EndFolk.SLEEPING);
        s.working = e.flag(EndFolk.WORKING);
        s.closed = e.flag(EndFolk.CLOSED);
        s.carrying = e.flag(EndFolk.CARRYING);
    }
}
