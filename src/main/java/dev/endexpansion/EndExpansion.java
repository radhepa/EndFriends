package dev.endexpansion;

import dev.endexpansion.court.CitadelLaw;
import dev.endexpansion.registry.MobRegistry;
import dev.endexpansion.anim.Cue;
import dev.endexpansion.talk.Conversation;
import dev.endexpansion.world.EndVillages;
import net.fabricmc.api.ModInitializer;
import net.fabricmc.fabric.api.event.lifecycle.v1.ServerLifecycleEvents;
import net.fabricmc.fabric.api.event.lifecycle.v1.ServerTickEvents;
import net.minecraft.resources.Identifier;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

/** End Expansion: villages, peoples and creatures for the outer End. */
public final class EndExpansion implements ModInitializer {
    public static final String MOD_ID = "endexpansion";
    public static final Logger LOG = LoggerFactory.getLogger("End Expansion");

    public static Identifier id(String path) {
        return Identifier.fromNamespaceAndPath(MOD_ID, path);
    }

    @Override
    public void onInitialize() {
        EndItems.register();
        EndEntities.register();
        MobRegistry.wireUp();
        EndVillages.register();
        Conversation.register();
        Cue.init();
        ServerTickEvents.END_SERVER_TICK.register(CitadelLaw::tick);
        ServerLifecycleEvents.SERVER_STOPPED.register(server -> CitadelLaw.clear());
    }
}
