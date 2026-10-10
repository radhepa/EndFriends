package dev.endexpansion.test;

import dev.endexpansion.anim.Clip;
import dev.endexpansion.anim.Cue;
import dev.endexpansion.anim.Library;
import dev.endexpansion.anim.Pack;
import dev.endexpansion.client.anim.Life;
import dev.endexpansion.entity.EndFolk;
import java.util.ArrayList;
import java.util.Comparator;
import java.util.List;
import java.util.Set;
import net.fabricmc.fabric.api.client.gametest.v1.FabricClientGameTest;
import net.fabricmc.fabric.api.client.gametest.v1.context.ClientGameTestContext;
import net.fabricmc.fabric.api.client.gametest.v1.context.TestServerContext;
import net.fabricmc.fabric.api.client.gametest.v1.context.TestSingleplayerContext;
import net.minecraft.client.Minecraft;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.world.entity.Entity;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.level.Level;
import net.minecraft.world.phys.AABB;

/**
 * The peoples' animation packs in a real game: every pack loads with fifty clips or more and something for every
 * moment; a row of each people (every look, and a child where they have them) acts out every clip in turn,
 * photographed mid-motion; and a reaction cue from the server plays for everyone watching.
 *   gradlew runClientGameTest -PendTests=Animations -PtestHeap=1536m
 */
@SuppressWarnings("UnstableApiUsage")
public class AnimationClientTest implements FabricClientGameTest {
    private static final int X = 3000, Y = 150, Z = 3000;

    /** Five grown-ups and (last) a child, or six grown-ups for the Court. */
    record Row(String people, List<String> types) {}

    private static final List<Row> ROWS = List.of(
            new Row("shulkin", List.of("shulkin", "shulkin", "shulkin", "shulkin", "shulkin", "shulkin_child")),
            new Row("chorrin", List.of("chorrin", "chorrin", "chorrin", "chorrin", "chorrin", "chorrin_child")),
            new Row("endarch", List.of("endarch_lord", "endarch_marshal", "endarch_riftguard", "endarch_lord", "endarch_marshal", "endarch_riftguard")));

    private static void check(boolean ok, String what) {
        VillagesClientTest.check(ok, what);
    }

    private static List<LivingEntity> row(Minecraft client, String people) {
        return client.level.getEntitiesOfClass(LivingEntity.class, new AABB(X - 12, Y - 4, Z - 4, X + 12, Y + 8, Z + 4),
                        e -> Life.kind(e) != null && Life.kind(e).species().equals(people)).stream()
                .sorted(Comparator.comparingDouble(Entity::getX)).toList();
    }

    @Override
    public void runTest(ClientGameTestContext ctx) {
        if (!VillagesClientTest.wanted("Animations", "endexpansion.tests", List.of())) return;
        ctx.getInput().resizeWindow(1600, 900);
        ctx.runOnClient(client -> {
            Library library = Library.current();
            for (String people : Library.SPECIES) {
                Pack pack = library.pack(people);
                check(pack != null, people + " has no animation pack");
                check(pack.clips().size() >= 50, people + " has only " + pack.clips().size() + " clips");
                for (String trigger : Pack.TRIGGERS) check(!library.clips(people, trigger).isEmpty(), people + " has no clip for " + trigger);
            }
        });
        try (TestSingleplayerContext world = ctx.worldBuilder().create()) {
            world.getConnection().waitForChunksRender(false, 2400);
            TestServerContext server = world.getServer();
            for (String cmd : List.of("gamerule spawn_mobs false", "time set 2000", "effect give @a night_vision infinite 0 true", "gamemode spectator @a")) {
                server.runCommand(cmd);
            }
            VillagesClientTest.tp(server, X, Y + 2, Z - 8, X, Y + 1.5, Z);
            ctx.waitTicks(40);
            world.getConnection().waitForChunksRender(false, 2400);
            server.runCommand(String.format("execute in minecraft:the_end run fill %d %d %d %d %d %d minecraft:purpur_block", X - 14, Y - 1, Z - 10, X + 14, Y - 1, Z + 6));
            server.runCommand(String.format("execute in minecraft:the_end run fill %d %d %d %d %d %d minecraft:end_stone_bricks", X - 14, Y, Z + 6, X + 14, Y + 6, Z + 6));
            ctx.runOnClient(client -> {
                if (!client.gui.hud.isHidden()) client.gui.hud.toggle();
            });
            List<String> report = new ArrayList<>();
            for (Row r : ROWS) {
                server.runCommand(String.format("execute in minecraft:the_end run kill @e[type=!player,x=%d,y=%d,z=%d,distance=..30]", X, Y, Z));
                for (int i = 0; i < r.types().size(); i++) {
                    server.runCommand(String.format("execute in minecraft:the_end run summon endexpansion:%s %.1f %d %.1f {NoAI:1b,PersistenceRequired:1b,Rotation:[180f,0f]}",
                            r.types().get(i), X + (i - (r.types().size() - 1) / 2.0) * 2.4, Y, Z + 0.5));
                }
                ctx.waitFor(client -> row(client, r.people()).size() == r.types().size(), 200);
                VillagesClientTest.tp(server, X, Y + (r.people().equals("endarch") ? 2.6 : 1.8), Z - 9.5, X, Y + (r.people().equals("endarch") ? 2.2 : 1.4), Z);
                ctx.waitTicks(20);
                List<Clip> clips = Library.current().pack(r.people()).clips();
                boolean children = r.types().getLast().endsWith("_child");
                List<Clip> young = children ? clips.stream().filter(c -> c.require().stream().anyMatch(g -> g.equals(Set.of("child")))).toList() : List.of();
                List<Clip> grown = clips.stream().filter(c -> !young.contains(c)).toList();
                int grownSlots = children ? r.types().size() - 1 : r.types().size();
                int shots = Math.max((grown.size() + grownSlots - 1) / grownSlots, young.size());
                for (int shot = 0; shot < shots; shot++) {
                    int first = shot * grownSlots, n = shot;
                    List<String> cast = ctx.computeOnClient(client -> {
                        List<LivingEntity> folk = row(client, r.people());
                        List<String> playing = new ArrayList<>();
                        for (int i = 0; i < folk.size(); i++) {
                            LivingEntity e = folk.get(i);
                            Clip clip = children && i == folk.size() - 1 ? (n < young.size() ? young.get(n) : grown.get(n % grown.size()))
                                    : first + i < grown.size() ? grown.get(first + i) : null;
                            if (clip == null) continue;
                            check(Life.of(e).play(e, clip.id()), r.people() + ": could not play " + clip.id());
                            playing.add(e.getId() + "=" + clip.id().substring(clip.id().indexOf(':') + 1));
                        }
                        return playing;
                    });
                    ctx.waitTicks(18);
                    ctx.runOnClient(client -> {
                        for (LivingEntity e : row(client, r.people())) {
                            String id = cast.stream().filter(c -> c.startsWith(e.getId() + "=")).findFirst().orElse(null);
                            if (id == null) continue;
                            var now = Life.of(e).activity();
                            check(now != null && now.id().endsWith(":" + id.substring(id.indexOf('=') + 1)), r.people() + ": " + id + " stopped before its photo");
                        }
                    });
                    String name = String.format("anim-%s-%02d", r.people(), shot + 1);
                    VillagesClientTest.shoot(ctx, name);
                    report.add(name + ": " + String.join(", ", cast));
                }
                server.runOnServer(srv -> {
                    ServerPlayer player = srv.getPlayerList().getPlayers().getFirst();
                    LivingEntity first = srv.getLevel(Level.END).getEntitiesOfClass(EndFolk.class,
                            new AABB(X - 12, Y - 4, Z - 4, X + 12, Y + 8, Z + 4), e -> true).getFirst();
                    Cue.send(first, "happy", player);
                });
                ctx.waitFor(client -> row(client, r.people()).stream().anyMatch(e -> Life.of(e).describe().endsWith("/happy")), 100);
                report.add(r.people() + ": " + clips.size() + " clips, happy cue played");
            }
            System.out.println("[endexpansion test] animations:" + System.lineSeparator() + String.join(System.lineSeparator(), report));
        }
    }
}
