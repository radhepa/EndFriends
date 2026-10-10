package dev.endexpansion.test;

import dev.endexpansion.EndEntities;
import dev.endexpansion.EndItems;
import dev.endexpansion.client.screen.ConversationScreen;
import dev.endexpansion.court.CitadelLaw;
import dev.endexpansion.court.CourtFavor;
import dev.endexpansion.entity.Chorrin;
import dev.endexpansion.entity.Driftray;
import dev.endexpansion.entity.EndFolk;
import dev.endexpansion.entity.Endarch;
import dev.endexpansion.entity.EndermanThrall;
import dev.endexpansion.entity.Groveback;
import dev.endexpansion.entity.Shulkin;
import dev.endexpansion.entity.Voidhound;
import dev.endexpansion.talk.Conversation;
import dev.endexpansion.talk.DialogueBank;
import dev.endexpansion.world.Settlement;
import java.util.Comparator;
import java.util.List;
import java.util.Map;
import net.fabricmc.fabric.api.client.gametest.v1.FabricClientGameTest;
import net.fabricmc.fabric.api.client.gametest.v1.context.ClientGameTestContext;
import net.fabricmc.fabric.api.client.gametest.v1.context.TestServerContext;
import net.fabricmc.fabric.api.client.gametest.v1.context.TestSingleplayerContext;
import net.minecraft.core.BlockPos;
import net.minecraft.core.registries.Registries;
import net.minecraft.resources.ResourceKey;
import net.minecraft.server.MinecraftServer;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.entity.Entity;
import net.minecraft.world.entity.EntitySpawnReason;
import net.minecraft.world.entity.EquipmentSlot;
import net.minecraft.world.entity.item.ItemEntity;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.Items;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.storage.loot.LootTable;
import net.minecraft.world.phys.AABB;

/**
 * The peoples and creatures in a real game: every mob lined up for a portrait, residents spawned by
 * their villages, conversations opened by right-click with replies and gifts pressed in the screen,
 * a Shulkin's lid, a Chorrin's blink, a Groveback's harvest, the Citadel's guest-law with and without
 * Enderman Eyes, a Court service task and the Lord's hound, and a Driftray tamed and saddled.
 *   gradlew runClientGameTest -PendTests=People -PtestHeap=1536m
 */
@SuppressWarnings("UnstableApiUsage")
public class PeopleClientTest implements FabricClientGameTest {
    private int shot = 1;

    private static void check(boolean ok, String what) {
        VillagesClientTest.check(ok, what);
    }

    private static void log(String what) {
        System.out.println("[endexpansion test] " + what);
    }

    private void shoot(ClientGameTestContext ctx, String name) {
        VillagesClientTest.shoot(ctx, String.format("people-%02d-%s", shot++, name));
    }

    /** Waits (in steps of half a second, up to {@code ticks}) until the server says yes: the server can lag behind the client here. */
    private static boolean eventually(ClientGameTestContext ctx, TestServerContext server, java.util.function.Function<MinecraftServer, Boolean> test, int ticks) {
        for (int t = 0; t < ticks; t += 10) {
            if (server.computeOnServer(test::apply)) return true;
            ctx.waitTicks(10);
        }
        return server.computeOnServer(test::apply);
    }

    private static ServerPlayer player(MinecraftServer srv) {
        return srv.getPlayerList().getPlayers().getFirst();
    }

    @Override
    public void runTest(ClientGameTestContext ctx) {
        if (!VillagesClientTest.wanted("People", "endexpansion.tests", List.of())) return;
        ctx.getInput().resizeWindow(1600, 900);
        ctx.runOnClient(client -> client.options.renderDistance().set(12));
        try (TestSingleplayerContext world = ctx.worldBuilder().adjustSettings(s -> {
            s.setGenerateStructures(true);
            s.setSeed(System.getProperty("endexpansion.seed", "20261009"));
        }).create()) {
            world.getConnection().waitForChunksRender(false, 2400);
            TestServerContext server = world.getServer();
            for (String cmd : List.of("gamerule spawn_mobs false", "time set 2000", "effect give @a night_vision infinite 0 true",
                    "effect give @a resistance infinite 4 true", "effect give @a regeneration infinite 4 true", "effect give @a saturation infinite 0 true")) {
                server.runCommand(cmd);
            }
            checkBanks();
            lineup(ctx, world, server);
            village(ctx, world, server, "spire_village");
            village(ctx, world, server, "stead_village");
            village(ctx, world, server, "crossing");
            citadel(ctx, world, server);
            driftray(ctx, world, server);
            checkLoot(server);
        }
    }

    // -- the dialogue bank ---------------------------------------------------------------------------

    private static void checkBanks() {
        for (String bank : List.of("shulkin", "chorrin", "shulkin_child", "chorrin_child", "court")) {
            DialogueBank b = DialogueBank.get(bank);
            check(b.has("greeting") && b.has("first_meeting"), bank + ": dialogue bank loaded with its topics");
            check(!b.names().isEmpty(), bank + ": has names");
        }
        check(!DialogueBank.get("court").places().isEmpty(), "court: has Citadel names");
    }

    // -- every mob, posed for a portrait ---------------------------------------------------------------

    private void lineup(ClientGameTestContext ctx, TestSingleplayerContext world, TestServerContext server) {
        int x = 3000, y = 150, z = 3000;
        server.runCommand("gamemode spectator @a");   // spectators don't fall while the camera is placed
        // commands only reach loaded ground: go there first
        VillagesClientTest.tp(server, x + 9, y + 2.5, z - 10, x + 9, y + 2, z);
        settle(ctx, world);
        server.runCommand(String.format("execute in minecraft:the_end run fill %d %d %d %d %d %d minecraft:purpur_block", x - 4, y - 1, z - 6, x + 46, y - 1, z + 30));
        server.runCommand(String.format("execute in minecraft:the_end run fill %d %d %d %d %d %d minecraft:end_rod", x - 4, y, z + 8, x + 46, y, z + 8));
        String[] people = {"shulkin", "shulkin_child", "chorrin", "chorrin_child", "endarch_lord", "endarch_marshal", "endarch_riftguard",
                "enderman_thrall", "groveback", "driftray", "voidhound"};
        int[] gap = {0, 4, 7, 11, 14, 19, 24, 29, 33, 38, 43};
        for (int i = 0; i < people.length; i++) {
            server.runCommand(String.format("execute in minecraft:the_end run summon endexpansion:%s %d %d %d {NoAI:1b,Rotation:[180f,0f],PersistenceRequired:1b}",
                    people[i], x + gap[i], y, z));
        }
        server.runCommand(String.format("execute in minecraft:the_end run summon endexpansion:voidhound %d %d %d {NoAI:1b,Age:-24000,Rotation:[180f,0f]}", x + 45, y, z - 2));
        int count = server.computeOnServer(srv -> srv.getLevel(Level.END).getEntitiesOfClass(Entity.class,
                new AABB(x - 6, y - 2, z - 8, x + 48, y + 8, z + 10), e -> e.getType().toString().contains("endexpansion")).size());
        check(count == people.length + 1, "all " + (people.length + 1) + " mobs spawn and stay (" + count + ")");
        ctx.runOnClient(client -> {
            if (!client.gui.hud.isHidden()) client.gui.hud.toggle();
        });
        // the peoples and the Court (x 0 to 29), then the creatures (29 to 46), facing the camera
        VillagesClientTest.tp(server, x + 14.5, y + 3.5, z - 16, x + 14.5, y + 1.8, z);
        settle(ctx, world);
        shoot(ctx, "peoples");
        VillagesClientTest.tp(server, x + 38, y + 2.8, z - 9, x + 38, y + 0.8, z);
        settle(ctx, world);
        shoot(ctx, "creatures");
        ctx.runOnClient(client -> {
            if (client.gui.hud.isHidden()) client.gui.hud.toggle();
        });
        VillagesClientTest.tp(server, x + 20, y, z + 15, x + 20, y, z + 25);
        server.runCommand("gamemode survival @a");
    }

    private static void settle(ClientGameTestContext ctx, TestSingleplayerContext world) {
        ctx.waitTicks(30);
        world.getConnection().waitForChunksRender(false, 2400);
        ctx.waitTicks(20);
    }

    // -- villages --------------------------------------------------------------------------------------

    /** Finds a village, goes there, and checks who lives in it; then talks to them. */
    private void village(ClientGameTestContext ctx, TestSingleplayerContext world, TestServerContext server, String kind) {
        var f = server.computeOnServer(srv -> VillagesClientTest.locate(srv, kind));
        check(f != null, kind + ": found");
        BlockPos o = f.origin();
        VillagesClientTest.tp(server, o.getX() + 0.5, o.getY() + 2, o.getZ() + 0.5, o.getX() + 8, o.getY() + 2, o.getZ() + 8);
        VillagesClientTest.settle(ctx, world, f);
        AABB box = new AABB(f.minX() - 8, o.getY() - 40, f.minZ() - 8, f.maxX() + 8, o.getY() + 60, f.maxZ() + 8);
        Map<String, Integer> census = server.computeOnServer(srv -> census(srv.getLevel(Level.END), box));
        log(kind + " census: " + census);
        int shulkin = census.getOrDefault("shulkin", 0), chorrin = census.getOrDefault("chorrin", 0);
        switch (kind) {
            case "spire_village" -> {
                check(shulkin >= 5, kind + ": Shulkin live here (" + shulkin + ")");
                check(chorrin == 0, kind + ": no Chorrin in a Spire");
            }
            case "stead_village" -> {
                check(chorrin >= 5, kind + ": Chorrin live here (" + chorrin + ")");
                check(shulkin == 0, kind + ": no Shulkin in a Stead");
            }
            default -> check(shulkin >= 2 && chorrin >= 2, kind + ": both peoples live here (" + shulkin + " Shulkin, " + chorrin + " Chorrin)");
        }
        check(census.getOrDefault("named", 0) > 0 && census.getOrDefault("settled", 0) == census.getOrDefault("folk", 0),
                kind + ": every resident has a name, a village and a home");
        String people = kind.startsWith("stead") ? "chorrin" : "shulkin";
        converse(ctx, server, o, people, false, kind);
        if (kind.startsWith("spire")) {
            converse(ctx, server, o, "shulkin", true, kind);
            lid(server, o);
        }
        if (kind.startsWith("stead")) {
            converse(ctx, server, o, "chorrin", true, kind);
            blink(server, o);
            groveback(server, o);
            night(ctx, world, server, o, f);
        }
    }

    private static Map<String, Integer> census(ServerLevel end, AABB box) {
        Map<String, Integer> out = new java.util.TreeMap<>();
        for (Entity e : end.getEntitiesOfClass(Entity.class, box, e -> e.getType().toString().contains("endexpansion"))) {
            String id = net.minecraft.core.registries.BuiltInRegistries.ENTITY_TYPE.getKey(e.getType()).getPath();
            out.merge(id, 1, Integer::sum);
            if (e instanceof EndFolk folk) {
                out.merge("folk", 1, Integer::sum);
                if (!folk.firstName().isEmpty()) out.merge("named", 1, Integer::sum);
                if (!folk.settlement().isWild() && folk.bed() != null) out.merge("settled", 1, Integer::sum);
                if (folk.isChild()) out.merge("children", 1, Integer::sum);
            }
        }
        return out;
    }

    /** The nearest resident of a people (adult or child) to a point, by entity id. */
    private static int nearest(TestServerContext server, BlockPos o, String people, boolean child, Class<? extends EndFolk> type) {
        return server.computeOnServer(srv -> srv.getLevel(Level.END).getEntitiesOfClass(type, new AABB(o).inflate(96),
                        e -> e.people().equals(people) && e.isChild() == child && e.isAlive() && !e.isSleeping())
                .stream().min(Comparator.comparingDouble((EndFolk e) -> e.distanceToSqr(net.minecraft.world.phys.Vec3.atCenterOf(o)))).map(Entity::getId).orElse(-1));
    }

    /** Walks up to a resident, right-clicks, reads the opening, asks something, gives a gift, says farewell. */
    private void converse(ClientGameTestContext ctx, TestServerContext server, BlockPos o, String people, boolean child, String kind) {
        int id = nearest(server, o, people, child, EndFolk.class);
        check(id >= 0, kind + ": found a " + (child ? "child" : "grown") + " " + people + " to talk to");
        faceAndTalk(ctx, server, id);
        var opened = ctx.computeOnClient(client -> ((ConversationScreen) client.gui.screen()).data());
        check(opened.dialogue().length() > 3 && !opened.dialogue().contains("{"), kind + ": the opening line is filled in: " + opened.dialogue());
        check(opened.voice().equals(child ? people + "_child" : people), kind + ": speaks in the " + opened.voice() + " voice");
        log(kind + ": " + opened.name() + " (" + opened.title() + ", " + opened.home() + "): " + opened.dialogue());
        waitTyped(ctx);
        shoot(ctx, (child ? people + "-child" : people) + "-hello");
        int before = bondPoints(server, id);
        press(ctx, "chat");
        var chatted = ctx.computeOnClient(client -> ((ConversationScreen) client.gui.screen()).data());
        check(bondPoints(server, id) > before, kind + ": a chat brings them closer (" + before + " -> " + bondPoints(server, id) + ")");
        log(kind + ": chat: " + chatted.dialogue());
        String topic = child ? "play" : "dragon";
        press(ctx, topic);
        log(kind + ": " + topic + ": " + ctx.computeOnClient(client -> ((ConversationScreen) client.gui.screen()).data().dialogue()));
        waitTyped(ctx);
        shoot(ctx, (child ? people + "-child" : people) + "-" + topic);
        // a gift they love, from their own bank
        String loved = child ? (people.equals("shulkin") ? "chorus_fruit" : "cookie") : (people.equals("shulkin") ? "end_rod" : "poppy");
        server.runOnServer(srv -> player(srv).setItemInHand(InteractionHand.MAIN_HAND,
                new ItemStack(net.minecraft.core.registries.BuiltInRegistries.ITEM.getValue(net.minecraft.resources.Identifier.withDefaultNamespace(loved)), 3)));
        int beforeGift = bondPoints(server, id);
        press(ctx, "gift");
        int afterGift = bondPoints(server, id);
        int left = server.computeOnServer(srv -> player(srv).getMainHandItem().getCount());
        log(kind + ": gift of " + loved + ": " + ctx.computeOnClient(client -> ((ConversationScreen) client.gui.screen()).data().status()));
        check(afterGift > beforeGift, kind + ": a gift they like brings them closer (" + beforeGift + " -> " + afterGift + ")");
        check(left == 2, kind + ": the gift left the player's hand");
        ctx.runOnClient(client -> client.gui.screen().onClose());
        ctx.waitTicks(10);
        boolean talking = server.computeOnServer(srv -> ((EndFolk) srv.getLevel(Level.END).getEntity(id)).flag(EndFolk.TALKING));
        check(!talking, kind + ": farewell ends the conversation");
    }

    /** Stands in the open beside a mob, looking at it, and right-clicks it (server side, as the click would). */
    private static void faceAndTalk(ClientGameTestContext ctx, TestServerContext server, int id) {
        server.runOnServer(srv -> {
            ServerLevel end = srv.getLevel(Level.END);
            Entity e = end.getEntity(id);
            var at = openSpotNear(end, e);
            lookFrom(srv, at, e);
        });
        ctx.waitTicks(10);
        server.runOnServer(srv -> {
            Entity e = srv.getLevel(Level.END).getEntity(id);
            e.interact(player(srv), InteractionHand.MAIN_HAND, e.position());
        });
        ctx.waitFor(client -> client.gui.screen() instanceof ConversationScreen, 100);
    }

    /** Puts the player at a spot, looking at a mob's face. */
    private static void lookFrom(MinecraftServer srv, net.minecraft.world.phys.Vec3 at, Entity e) {
        double dx = e.getX() - at.x, dz = e.getZ() - at.z, dy = (e.getEyeY() - 0.15) - (at.y + 1.62);
        float yaw = (float) Math.toDegrees(Math.atan2(-dx, dz));
        float pitch = (float) -Math.toDegrees(Math.atan2(dy, Math.sqrt(dx * dx + dz * dz)));
        srv.getCommands().performPrefixedCommand(srv.createCommandSourceStack(), String.format(java.util.Locale.ROOT,
                "execute in minecraft:the_end run tp @a %.2f %.2f %.2f %.1f %.1f", at.x, at.y, at.z, yaw, pitch));
    }

    /** Somewhere a player can stand 2-4 blocks from a mob, in front of it if there's room. */
    private static net.minecraft.world.phys.Vec3 openSpotNear(ServerLevel level, Entity e) {
        float face = e.getYRot();
        for (double r : new double[] {3.0, 2.5, 4.0}) {
            for (int turn = 0; turn < 360; turn += 30) {
                double a = Math.toRadians(face + (turn % 60 == 0 ? turn / 2 : -turn / 2 - 15));
                double x = e.getX() - Math.sin(a) * r, z = e.getZ() + Math.cos(a) * r;
                for (int dy = 1; dy >= -2; dy--) {
                    double y = Math.floor(e.getY()) + dy;
                    AABB body = new AABB(x - 0.3, y, z - 0.3, x + 0.3, y + 1.8, z + 0.3);
                    BlockPos under = BlockPos.containing(x, y - 0.5, z);
                    var eye = new net.minecraft.world.phys.Vec3(x, y + 1.62, z);
                    boolean seen = level.clip(new net.minecraft.world.level.ClipContext(eye, e.getEyePosition(),
                            net.minecraft.world.level.ClipContext.Block.COLLIDER, net.minecraft.world.level.ClipContext.Fluid.NONE, e))
                            .getType() == net.minecraft.world.phys.HitResult.Type.MISS;
                    if (seen && level.noCollision(body) && !level.getBlockState(under).getCollisionShape(level, under).isEmpty()) {
                        return new net.minecraft.world.phys.Vec3(x, y, z);
                    }
                }
            }
        }
        return e.position().add(0, 0.2, 0);
    }

    /** Shows the whole line (this machine draws few frames in a test) and waits until it is on screen. */
    private static void waitTyped(ClientGameTestContext ctx) {
        ctx.runOnClient(client -> {
            if (client.gui.screen() instanceof ConversationScreen s) s.showWholeLines();
        });
        ctx.waitFor(client -> !(client.gui.screen() instanceof ConversationScreen s) || s.doneTyping(), 200);
        check(ctx.computeOnClient(client -> client.gui.screen() instanceof ConversationScreen), "the conversation is still open");
        ctx.waitTicks(3);
    }

    /** Presses a reply or dock button and waits for the answer. */
    private static void press(ClientGameTestContext ctx, String action) {
        String before = ctx.computeOnClient(client -> ((ConversationScreen) client.gui.screen()).data().toString());
        ctx.runOnClient(client -> ((ConversationScreen) client.gui.screen()).press(action));
        ctx.waitFor(client -> client.gui.screen() instanceof ConversationScreen s && !s.data().toString().equals(before), 100);
    }

    private static int bondPoints(TestServerContext server, int id) {
        return server.computeOnServer(srv -> {
            EndFolk folk = (EndFolk) srv.getLevel(Level.END).getEntity(id);
            return folk.bond(player(srv)).points;
        });
    }

    private static void lid(TestServerContext server, BlockPos o) {
        int id = nearest(server, o, "shulkin", false, Shulkin.class);
        boolean closed = server.computeOnServer(srv -> {
            ServerLevel end = srv.getLevel(Level.END);
            Shulkin s = (Shulkin) end.getEntity(id);
            s.hurtServer(end, end.damageSources().generic(), 2.0F);
            return s.isClosed();
        });
        check(closed, "a hurt Shulkin shuts its lid");
    }

    private static void blink(TestServerContext server, BlockPos o) {
        int id = nearest(server, o, "chorrin", false, Chorrin.class);
        double moved = server.computeOnServer(srv -> {
            ServerLevel end = srv.getLevel(Level.END);
            Chorrin c = (Chorrin) end.getEntity(id);
            var from = c.position();
            c.hurtServer(end, end.damageSources().generic(), 1.0F);
            return c.position().distanceTo(from);
        });
        check(moved > 1.5, "a startled Chorrin blinks away (" + String.format("%.1f", moved) + " blocks)");
    }

    private static void groveback(TestServerContext server, BlockPos o) {
        String result = server.computeOnServer(srv -> {
            ServerLevel end = srv.getLevel(Level.END);
            var herd = end.getEntitiesOfClass(Groveback.class, new AABB(o).inflate(96), Groveback::isRipe);
            ServerPlayer p = player(srv);
            Groveback g;
            if (herd.isEmpty()) {
                // not every Stead layout has a pen: bring one
                g = EndEntities.GROVEBACK.create(end, EntitySpawnReason.COMMAND);
                g.snapTo(p.getX(), p.getY(), p.getZ(), 0, 0);
                end.addFreshEntity(g);
                log("this Stead has no herd; a Groveback was brought for the harvest");
            } else {
                g = herd.getFirst();
                log("harvesting a Groveback of the village herd (" + herd.size() + " ripe)");
            }
            p.setItemInHand(InteractionHand.MAIN_HAND, ItemStack.EMPTY);
            p.teleportTo(end, g.getX() + 1.5, g.getY(), g.getZ(), java.util.Set.of(), 0, 0, false);
            g.mobInteract(p, InteractionHand.MAIN_HAND);
            int fruit = end.getEntitiesOfClass(ItemEntity.class, g.getBoundingBox().inflate(4), i -> i.getItem().is(Items.CHORUS_FRUIT))
                    .stream().mapToInt(i -> i.getItem().getCount()).sum();
            return fruit >= 2 && !g.isRipe() ? "ok" : "picked " + fruit + " fruit, ripe " + g.isRipe();
        });
        check(result.equals("ok"), "a Groveback's back gives chorus fruit and then grows back (" + result + ")");
    }

    /** At night, residents go home and sleep (the player stays away so nobody needs to walk in sight). */
    private void night(ClientGameTestContext ctx, TestSingleplayerContext world, TestServerContext server, BlockPos o, VillagesClientTest.Found f) {
        server.runCommand("time set 14000");
        VillagesClientTest.tp(server, o.getX() + 95, o.getY() + 30, o.getZ(), o.getX(), o.getY(), o.getZ());
        java.util.function.Function<MinecraftServer, int[]> count = srv -> {
            var folk = srv.getLevel(Level.END).getEntitiesOfClass(EndFolk.class, new AABB(o).inflate(80), e -> e.bed() != null);
            return new int[] {(int) folk.stream().filter(EndFolk::isSleeping).count(), folk.size()};
        };
        eventually(ctx, server, srv -> {
            int[] n = count.apply(srv);
            return n[0] * 4 >= n[1] * 3;
        }, 3000);
        int[] asleep = server.computeOnServer(count::apply);
        log("asleep at night: " + asleep[0] + " of " + asleep[1]);
        check(asleep[0] * 2 >= asleep[1], "at night most residents are asleep at home (" + asleep[0] + " of " + asleep[1] + ")");
        int sleeper = server.computeOnServer(srv -> srv.getLevel(Level.END).getEntitiesOfClass(EndFolk.class, new AABB(o).inflate(80), EndFolk::isSleeping)
                .stream().findFirst().map(Entity::getId).orElse(-1));
        if (sleeper >= 0) {
            server.runOnServer(srv -> {
                Entity e = srv.getLevel(Level.END).getEntity(sleeper);
                lookFrom(srv, openSpotNear(srv.getLevel(Level.END), e), e);
            });
            settle(ctx, world);
            shoot(ctx, "chorrin-asleep");
        }
        server.runCommand("time set 2000");
    }

    // -- the Citadel -----------------------------------------------------------------------------------

    private void citadel(ClientGameTestContext ctx, TestSingleplayerContext world, TestServerContext server) {
        var f = server.computeOnServer(srv -> VillagesClientTest.locate(srv, "citadel"));
        check(f != null, "citadel: found");
        BlockPos o = f.origin();
        server.runCommand("clear @a");
        // outside first, to load it and count the Court
        VillagesClientTest.tp(server, o.getX(), o.getY() + 40, o.getZ() - 90, o.getX(), o.getY(), o.getZ());
        VillagesClientTest.settle(ctx, world, f);
        AABB box = new AABB(f.minX() - 8, o.getY() - 40, f.minZ() - 8, f.maxX() + 8, o.getY() + 60, f.maxZ() + 8);
        Map<String, Integer> census = server.computeOnServer(srv -> census(srv.getLevel(Level.END), box));
        log("citadel census: " + census);
        check(census.getOrDefault("endarch_lord", 0) == 1, "citadel: one Lord");
        check(census.getOrDefault("endarch_riftguard", 0) >= 4, "citadel: Riftguards");
        check(census.getOrDefault("enderman_thrall", 0) >= 3, "citadel: thralls");
        check(census.getOrDefault("voidhound", 0) >= 2, "citadel: hounds");
        check(census.getOrDefault("shulkin", 0) + census.getOrDefault("chorrin", 0) == 0, "citadel: no Shulkin or Chorrin");

        // 1. without the Eyes: the alarm, and the Court attacks
        BlockPos court = o.offset(0, 1, -17);
        VillagesClientTest.tp(server, court.getX() + 0.5, court.getY() + 0.5, court.getZ() + 0.5, o.getX(), o.getY() + 3, o.getZ() + 10);
        Settlement citadel = server.computeOnServer(srv -> srv.getLevel(Level.END).getEntitiesOfClass(Endarch.class, box, e -> true)
                .getFirst().settlement());
        check(eventually(ctx, server, srv -> CitadelLaw.isOutlawAt(player(srv), citadel), 200), "citadel: crossing in without the Eyes makes you an outlaw");
        int hunters = 0;
        for (int i = 0; i < 20 && hunters == 0; i++) {
            ctx.waitTicks(20);
            hunters = server.computeOnServer(srv -> {
                ServerPlayer p = player(srv);
                return srv.getLevel(Level.END).getEntitiesOfClass(net.minecraft.world.entity.Mob.class, box, m -> m.getTarget() == p).size();
            });
        }
        check(hunters > 0, "citadel: the Court comes for an outlaw (" + hunters + " hunting)");
        shoot(ctx, "citadel-alarm");
        // 2. leaving lifts it
        VillagesClientTest.tp(server, o.getX() + 400, o.getY() + 60, o.getZ(), o.getX(), o.getY(), o.getZ());
        check(eventually(ctx, server, srv -> !CitadelLaw.isOutlawAt(player(srv), citadel), 200), "citadel: an outlaw who leaves is let be");
        // 3. with the Eyes: a guest
        server.runCommand("give @a endexpansion:enderman_eyes");
        VillagesClientTest.tp(server, court.getX() + 0.5, court.getY() + 0.5, court.getZ() + 0.5, o.getX(), o.getY() + 3, o.getZ() + 10);
        ctx.waitTicks(60);
        check(!server.computeOnServer(srv -> CitadelLaw.isOutlawAt(player(srv), citadel)), "citadel: a guest bearing the Eyes is received");
        int lord = server.computeOnServer(srv -> srv.getLevel(Level.END).getEntitiesOfClass(Endarch.class, box, e -> e.job().equals("lord"))
                .stream().findFirst().map(Entity::getId).orElse(-1));
        check(lord >= 0, "citadel: the Lord is on the throne");
        faceAndTalk(ctx, server, lord);
        var audience = ctx.computeOnClient(client -> ((ConversationScreen) client.gui.screen()).data());
        check(audience.voice().equals("court") && audience.meter().equals("eye"), "citadel: the Lord speaks as the Court, with Favor as eyes");
        log("citadel: " + audience.name() + ": " + audience.dialogue());
        waitTyped(ctx);
        shoot(ctx, "lord-audience");
        // a service task, delivered
        press(ctx, "service");
        String task = server.computeOnServer(srv -> CourtFavor.get(srv).bond(citadel.key(), player(srv).getUUID()).task);
        check(!task.isEmpty(), "citadel: the Court sets a task (" + task + ")");
        var t = Conversation.TASKS.stream().filter(x -> x.id().equals(task)).findFirst().orElseThrow();
        int favorBefore = server.computeOnServer(srv -> CourtFavor.get(srv).bond(citadel.key(), player(srv).getUUID()).points);
        server.runOnServer(srv -> player(srv).getInventory().add(new ItemStack(t.item(), t.count())));
        press(ctx, "service");
        int favorAfter = server.computeOnServer(srv -> CourtFavor.get(srv).bond(citadel.key(), player(srv).getUUID()).points);
        check(favorAfter >= favorBefore + t.favor(), "citadel: delivering the task earns Favor (" + favorBefore + " -> " + favorAfter + ")");
        // high Favor: the Lord's hound
        server.runOnServer(srv -> CourtFavor.get(srv).bond(citadel.key(), player(srv).getUUID()).points = 140);
        press(ctx, "hound");
        boolean pup = server.computeOnServer(srv -> {
            ServerPlayer p = player(srv);
            return !srv.getLevel(Level.END).getEntitiesOfClass(Voidhound.class, p.getBoundingBox().inflate(6), h -> h.isOwnedBy(p) && h.isBaby()).isEmpty();
        });
        check(pup, "citadel: at high Favor the Lord gives a Voidhound pup");
        waitTyped(ctx);
        shoot(ctx, "lord-hound");
        ctx.runOnClient(client -> client.gui.screen().onClose());
        ctx.waitTicks(10);
        server.runOnServer(srv -> {
            ServerPlayer p = player(srv);
            var pups = srv.getLevel(Level.END).getEntitiesOfClass(Voidhound.class, p.getBoundingBox().inflate(8), h -> h.isOwnedBy(p));
            if (!pups.isEmpty()) lookFrom(srv, openSpotNear(srv.getLevel(Level.END), pups.getFirst()), pups.getFirst());
        });
        settle(ctx, world);
        shoot(ctx, "voidhound-pup");
        // a thrall won't talk
        int thrall = server.computeOnServer(srv -> srv.getLevel(Level.END).getEntitiesOfClass(EndermanThrall.class, box, e -> true)
                .stream().findFirst().map(Entity::getId).orElse(-1));
        server.runOnServer(srv -> srv.getLevel(Level.END).getEntity(thrall).interact(player(srv), InteractionHand.MAIN_HAND, player(srv).position()));
        ctx.waitTicks(5);
        check(ctx.computeOnClient(client -> !(client.gui.screen() instanceof ConversationScreen)), "citadel: a thrall won't talk");
        // 4. losing the Eyes inside ends guest-law
        server.runCommand("clear @a endexpansion:enderman_eyes");
        check(eventually(ctx, server, srv -> CitadelLaw.isOutlawAt(player(srv), citadel), 200), "citadel: losing the Eyes inside ends guest-law");
        VillagesClientTest.tp(server, o.getX() + 400, o.getY() + 60, o.getZ(), o.getX(), o.getY(), o.getZ());
        ctx.waitTicks(40);
    }

    // -- a Driftray, tamed and saddled -----------------------------------------------------------------

    private void driftray(ClientGameTestContext ctx, TestSingleplayerContext world, TestServerContext server) {
        int x = 3020, y = 150, z = 3020;   // on the lineup's platform
        VillagesClientTest.tp(server, x + 5, y, z - 4, x, y + 1, z);
        settle(ctx, world);
        server.runCommand(String.format("execute in minecraft:the_end run fill %d %d %d %d %d %d minecraft:end_stone", x - 6, y - 1, z - 6, x + 6, y - 1, z + 6));
        String result = server.computeOnServer(srv -> {
            ServerLevel end = srv.getLevel(Level.END);
            Driftray ray = EndEntities.DRIFTRAY.create(end, EntitySpawnReason.COMMAND);
            ray.snapTo(x + 0.5, y, z + 0.5, 0, 0);
            end.addFreshEntity(ray);
            ServerPlayer p = player(srv);
            p.teleportTo(end, x + 2.5, y, z + 0.5, java.util.Set.of(), 90, 0, false);
            for (int i = 0; i < 10 && !ray.isTamed(); i++) {
                p.setItemInHand(InteractionHand.MAIN_HAND, new ItemStack(Items.CHORUS_FLOWER));
                ray.mobInteract(p, InteractionHand.MAIN_HAND);
            }
            if (!ray.isTamed()) return "not tamed by chorus flowers";
            ray.setItemSlot(EquipmentSlot.SADDLE, new ItemStack(Items.SADDLE));
            if (!p.startRiding(ray)) return "could not ride";
            return "ok:" + ray.getId();
        });
        check(result.startsWith("ok"), "driftray: tamed with chorus flowers, saddled and ridden (" + result + ")");
        int id = Integer.parseInt(result.substring(3));
        server.runOnServer(srv -> player(srv).stopRiding());
        eventually(ctx, server, srv -> {
            double h = srv.getLevel(Level.END).getEntity(id).getY() - y;
            return h > 1.0 && h < 4.0;
        }, 400);
        double height = server.computeOnServer(srv -> srv.getLevel(Level.END).getEntity(id).getY() - y);
        check(height > 0.3 && height < 4.0, "driftray: hovers over the ground on its own (" + String.format("%.1f", height) + " up)");
        VillagesClientTest.tp(server, x + 5, y, z - 4, x, y + 2, z);
        settle(ctx, world);
        shoot(ctx, "driftray-tamed");
    }

    private static void checkLoot(TestServerContext server) {
        boolean ok = server.computeOnServer(srv -> {
            LootTable table = srv.reloadableRegistries().getLootTable(ResourceKey.create(Registries.LOOT_TABLE, dev.endexpansion.EndExpansion.id("chests/envoy_ship")));
            return table != LootTable.EMPTY;
        });
        check(ok, "the envoy ship chest loot table loads");
        log("all People checks passed");
        check(EndItems.ENDERMAN_EYES != null, "Enderman Eyes are registered");
    }
}
