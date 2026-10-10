package dev.endexpansion.test;

import dev.endexpansion.EndExpansion;
import dev.endexpansion.world.VillagePieces;
import java.util.ArrayList;
import java.util.List;
import net.fabricmc.fabric.api.client.gametest.v1.FabricClientGameTest;
import net.fabricmc.fabric.api.client.gametest.v1.context.ClientGameTestContext;
import net.fabricmc.fabric.api.client.gametest.v1.context.TestServerContext;
import net.fabricmc.fabric.api.client.gametest.v1.context.TestSingleplayerContext;
import net.minecraft.core.BlockPos;
import net.minecraft.core.HolderSet;
import net.minecraft.core.registries.Registries;
import net.minecraft.resources.ResourceKey;
import net.minecraft.server.MinecraftServer;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.block.Blocks;
import net.minecraft.world.level.levelgen.structure.Structure;
import net.minecraft.world.level.levelgen.structure.StructureStart;

/**
 * Finds every End village kind in a fresh world's outer End (natural generation, not /place),
 * checks it was built (ground piece, tiles, the people's blocks), and photographs it from above,
 * from the street and from below the islets. Screenshots land in build/run/clientGameTest/screenshots.
 *   gradlew runClientGameTest -PendTests=Villages [-PendKinds=spire_village,citadel] -PtestHeap=2g
 */
@SuppressWarnings("UnstableApiUsage")
public class VillagesClientTest implements FabricClientGameTest {
    static final List<String> KINDS = List.of("spire_village", "stead_village", "crossing", "citadel");

    static void check(boolean ok, String what) {
        if (!ok) throw new AssertionError(what);
        System.out.println("[endexpansion test] ok: " + what);
    }

    static boolean wanted(String name, String property, List<String> all) {
        String only = System.getProperty(property);
        return only == null || only.isBlank() || List.of(only.split(",")).contains(name);
    }

    static void shoot(ClientGameTestContext ctx, String name) {
        ctx.runOnClient(client -> client.gui.toastManager().clear());
        ctx.takeScreenshot(name);
    }

    /** What the test learned about one village. */
    record Found(String kind, BlockPos origin, int pieces, int minX, int minZ, int maxX, int maxZ) {}

    @Override
    public void runTest(ClientGameTestContext ctx) {
        if (!wanted("Villages", "endexpansion.tests", List.of())) return;
        ctx.getInput().resizeWindow(1600, 900);
        // the integrated server takes its view distance from this when the world starts
        ctx.runOnClient(client -> client.options.renderDistance().set(16));
        // consistent test settings switch structures off; villages need them on (a fixed seed keeps runs comparable)
        try (TestSingleplayerContext world = ctx.worldBuilder().adjustSettings(s -> {
            s.setGenerateStructures(true);
            s.setSeed(System.getProperty("endexpansion.seed", "20261009"));
        }).create()) {
            world.getConnection().waitForChunksRender(false, 2400);
            ctx.runOnClient(client -> {
                if (!client.gui.hud.isHidden()) client.gui.hud.toggle();
            });
            TestServerContext server = world.getServer();
            for (String cmd : List.of("gamemode spectator @a", "gamerule spawn_mobs false", "effect give @a night_vision infinite 0 true")) {
                server.runCommand(cmd);
            }
            List<Found> found = new ArrayList<>();
            int shot = 1;
            for (String kind : KINDS) {
                if (!wanted(kind, "endexpansion.kinds", KINDS)) continue;
                Found f = server.computeOnServer(srv -> locate(srv, kind));
                System.out.println("[endexpansion test] site verdicts: " + dev.endexpansion.world.EndVillageStructure.VERDICTS);
                check(f != null, kind + ": found a village in the outer End");
                System.out.println("[endexpansion test] " + kind + " at " + f.origin() + " with " + f.pieces() + " pieces");
                found.add(f);
                BlockPos o = f.origin();
                int span = Math.max(f.maxX() - f.minX(), f.maxZ() - f.minZ());
                // overview from the north-west, high
                tp(server, o.getX() - span * 0.5, o.getY() + span * 0.5, o.getZ() - span * 0.5, o.getX(), o.getY() + 2, o.getZ());
                settle(ctx, world, f);
                shoot(ctx, String.format("end-%02d-%s-overview", shot++, kind));
                // from the opposite side, lower
                tp(server, o.getX() + span * 0.55, o.getY() + span * 0.2, o.getZ() + span * 0.45, o.getX(), o.getY() + 8, o.getZ());
                settle(ctx, world, f);
                shoot(ctx, String.format("end-%02d-%s-side", shot++, kind));
                // standing at the edge of the centre, looking across it
                tp(server, o.getX() - 11.5, o.getY() + 2.6, o.getZ() - 11.5, o.getX() + 14, o.getY() + 6, o.getZ() + 14);
                settle(ctx, world, f);
                shoot(ctx, String.format("end-%02d-%s-street", shot++, kind));
                // from out in the void, below the rim: the islets hanging under the village
                tp(server, o.getX() + span * 0.75, o.getY() - span * 0.16, o.getZ() - span * 0.3, o.getX(), o.getY() - 6, o.getZ());
                settle(ctx, world, f);
                shoot(ctx, String.format("end-%02d-%s-below", shot++, kind));
            }
            check(!found.isEmpty(), "at least one village kind was tested");
        }
    }

    static void tp(TestServerContext server, double x, double y, double z, double lx, double ly, double lz) {
        server.runCommand(String.format("execute in minecraft:the_end run tp @a %.1f %.1f %.1f facing %.1f %.1f %.1f", x, y, z, lx, ly, lz));
    }

    static void settle(ClientGameTestContext ctx, TestSingleplayerContext world, Found f) {
        ctx.waitTicks(40);
        // wait (at most a minute) until the client holds the village's chunks, then let them render
        int missing = -1;
        for (int i = 0; i < 60; i++) {
            missing = ctx.computeOnClient(client -> {
                int n = 0;
                if (client.level == null) return 9999;
                for (int cx = f.minX() >> 4; cx <= f.maxX() >> 4; cx++)
                    for (int cz = f.minZ() >> 4; cz <= f.maxZ() >> 4; cz++)
                        if (!client.level.getChunkSource().hasChunk(cx, cz)) n++;
                return n;
            });
            if (missing == 0) break;
            ctx.waitTicks(20);
        }
        System.out.println("[endexpansion test] village chunks still missing on the client: " + missing);
        // chunks out in the End generate slowly on a test machine: allow two minutes
        world.getConnection().waitForChunksRender(false, 2400);
        ctx.waitTicks(40);
    }

    /** Locate the nearest village of a kind east of the main island, generate it and check its blocks. */
    static Found locate(MinecraftServer srv, String kind) {
        ServerLevel end = srv.getLevel(Level.END);
        var registry = srv.registryAccess().lookupOrThrow(Registries.STRUCTURE);
        var holder = registry.getOrThrow(ResourceKey.create(Registries.STRUCTURE, EndExpansion.id(kind)));
        BlockPos near = end.findNearestMapStructure(HolderSet.direct(holder), new BlockPos(1400, 64, 0), 120, false);
        if (near == null) return null;
        Structure structure = holder.value();
        StructureStart start = end.getChunk(near.getX() >> 4, near.getZ() >> 4).getStartForStructure(structure);
        check(start != null && start.isValid(), kind + ": structure start at " + near);
        var pieces = start.getPieces();
        check(pieces.getFirst() instanceof VillagePieces.GroundPiece, kind + ": the ground piece comes first");
        check(pieces.size() >= 2, kind + ": has tiles (" + (pieces.size() - 1) + ")");
        var ground = (VillagePieces.GroundPiece) pieces.getFirst();
        var box = start.getBoundingBox();
        // generate every chunk of the village
        for (int cx = box.minX() >> 4; cx <= box.maxX() >> 4; cx++)
            for (int cz = box.minZ() >> 4; cz <= box.maxZ() >> 4; cz++)
                end.getChunk(cx, cz);
        BlockPos o = ground.origin();
        int built = 0, stone = 0;
        var pos = new BlockPos.MutableBlockPos();
        for (int x = box.minX(); x <= box.maxX(); x += 2)
            for (int z = box.minZ(); z <= box.maxZ(); z += 2)
                for (int y = o.getY() - 2; y <= Math.min(box.maxY(), o.getY() + 40); y++) {
                    var s = end.getBlockState(pos.set(x, y, z));
                    if (s.is(Blocks.END_STONE)) stone++;
                    else if (!s.isAir()) built++;
                }
        check(built > 300, kind + ": village blocks were placed (" + built + " sampled)");
        check(!end.getBlockState(o).isAir(), kind + ": the village floor is solid at the centre " + o);
        System.out.println("[endexpansion test] " + kind + ": sampled " + built + " built blocks, " + stone + " end stone");
        return new Found(kind, o, pieces.size(), box.minX(), box.minZ(), box.maxX(), box.maxZ());
    }
}
