package dev.endexpansion.client;

import dev.endexpansion.EndEntities;
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

        ClientPlayNetworking.registerGlobalReceiver(TalkPayload.TYPE, (payload, context) -> {
            var client = context.client();
            if (client.gui.screen() instanceof ConversationScreen screen && screen.matches(payload)) screen.update(payload);
            else if (payload.opening() && client.player != null) client.gui.setScreen(new ConversationScreen(payload));
        });
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
