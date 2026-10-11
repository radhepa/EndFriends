package dev.endexpansion.test;

import java.util.HashMap;
import java.util.LinkedHashMap;
import java.util.Map;
import net.fabricmc.fabric.api.client.gametest.v1.FabricClientGameTest;
import net.fabricmc.fabric.api.client.gametest.v1.context.ClientGameTestContext;
import net.fabricmc.fabric.api.client.gametest.v1.context.TestSingleplayerContext;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.core.registries.Registries;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.world.entity.EntitySpawnReason;
import net.minecraft.world.entity.EquipmentSlot;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.Items;
import net.minecraft.world.item.enchantment.Enchantments;
import net.minecraft.world.level.storage.loot.LootParams;
import net.minecraft.world.level.storage.loot.LootTable;
import net.minecraft.world.level.storage.loot.parameters.LootContextParamSets;
import net.minecraft.world.level.storage.loot.parameters.LootContextParams;
import net.minecraft.world.phys.Vec3;

/**
 * Every End Expansion loot table rolled hundreds of times in a real world, so we know Minecraft 26.3 reads
 * it (26.3 silently skips 1.21's "functions"/"conditions" keys): each mob's drop counts vary as set_count
 * says, Looting III adds to them, and the envoy ship's chest holds Enderman Eyes and End city treasure.
 *   gradlew runClientGameTest -PendTests=Loot
 */
@SuppressWarnings("UnstableApiUsage")
public class LootClientTest implements FabricClientGameTest {
    static final int ROLLS = 300;

    /** Per item: in how many rolls it came, its biggest stack and how many in all. */
    static Map<Item, int[]> roll(LootTable table, LootParams params) {
        Map<Item, int[]> out = new LinkedHashMap<>();
        for (int i = 0; i < ROLLS; i++) {
            Map<Item, Integer> got = new HashMap<>();
            for (ItemStack stack : table.getRandomItems(params)) if (!stack.isEmpty()) got.merge(stack.getItem(), stack.getCount(), Integer::sum);
            got.forEach((item, n) -> {
                int[] t = out.computeIfAbsent(item, k -> new int[3]);
                t[0]++; t[1] = Math.max(t[1], n); t[2] += n;
            });
        }
        return out;
    }

    static int total(Map<Item, int[]> tally) { return tally.values().stream().mapToInt(t -> t[2]).sum(); }

    static String show(Map<Item, int[]> tally) {
        StringBuilder s = new StringBuilder();
        tally.forEach((item, t) -> s.append(BuiltInRegistries.ITEM.getKey(item).getPath()).append(" in ").append(t[0])
                .append(" up to ").append(t[1]).append(" (").append(t[2]).append(") "));
        return s.toString().trim();
    }

    @Override
    public void runTest(ClientGameTestContext ctx) {
        if (!VillagesClientTest.wanted("Loot", "endexpansion.tests", java.util.List.of())) return;
        try (TestSingleplayerContext world = ctx.worldBuilder().create()) {
            world.getConnection().waitForChunksRender();
            world.getServer().runOnServer(srv -> {
                ServerLevel level = srv.overworld();
                ServerPlayer player = srv.getPlayerList().getPlayers().getFirst();
                Vec3 origin = player.position();
                var tables = srv.reloadableRegistries().lookup().lookupOrThrow(Registries.LOOT_TABLE).listElementIds()
                        .filter(k -> k.identifier().getNamespace().equals("endexpansion")).sorted((a, b) -> a.identifier().compareTo(b.identifier())).toList();
                VillagesClientTest.check(tables.size() == 12, "12 End Expansion loot tables load, found " + tables.size());
                ItemStack looting = new ItemStack(Items.DIAMOND_SWORD);
                looting.enchant(srv.registryAccess().lookupOrThrow(Registries.ENCHANTMENT).getOrThrow(Enchantments.LOOTING), 3);
                for (var key : tables) {
                    LootTable table = srv.reloadableRegistries().getLootTable(key);
                    String path = key.identifier().getPath();
                    if (path.startsWith("chests/")) {
                        var got = roll(table, new LootParams.Builder(level).withParameter(LootContextParams.ORIGIN, origin).create(LootContextParamSets.CHEST));
                        System.out.println("[endexpansion test] " + path + ": " + show(got));
                        int[] eyes = got.get(BuiltInRegistries.ITEM.getValue(net.minecraft.resources.Identifier.parse("endexpansion:enderman_eyes")));
                        VillagesClientTest.check(eyes != null && eyes[0] == ROLLS && got.size() > 3, path + " always holds Enderman Eyes beside End city treasure");
                        continue;
                    }
                    var type = BuiltInRegistries.ENTITY_TYPE.getOptional(key.identifier().withPath(path.substring("entities/".length()))).orElseThrow();
                    var mob = type.create(level, EntitySpawnReason.COMMAND);
                    VillagesClientTest.check(mob != null, path + " belongs to a mob");
                    mob.setPos(origin);
                    player.setItemSlot(EquipmentSlot.MAINHAND, ItemStack.EMPTY);
                    var bare = roll(table, kill(level, mob, player, origin));
                    player.setItemSlot(EquipmentSlot.MAINHAND, looting.copy());
                    var lucky = roll(table, kill(level, mob, player, origin));
                    player.setItemSlot(EquipmentSlot.MAINHAND, ItemStack.EMPTY);
                    System.out.println("[endexpansion test] " + path + ": " + show(bare) + " | Looting III: " + show(lucky));
                    if (bare.isEmpty()) {
                        VillagesClientTest.check(lucky.isEmpty(), path + " drops nothing (a child)");
                        continue;
                    }
                    // Before 26.3's keys every drop was exactly one of each item, every time.
                    VillagesClientTest.check(bare.values().stream().anyMatch(t -> t[1] >= 2 || t[0] < ROLLS), path + " drop counts follow set_count: " + show(bare));
                    VillagesClientTest.check(total(lucky) - total(bare) > ROLLS * bare.size(), path + " Looting III adds about 1.5 of each drop: "
                            + total(bare) + " -> " + total(lucky));
                }
            });
        }
    }

    static LootParams kill(ServerLevel level, net.minecraft.world.entity.Entity mob, ServerPlayer player, Vec3 origin) {
        return new LootParams.Builder(level).withParameter(LootContextParams.THIS_ENTITY, mob).withParameter(LootContextParams.ORIGIN, origin)
                .withParameter(LootContextParams.DAMAGE_SOURCE, level.damageSources().playerAttack(player))
                .withParameter(LootContextParams.ATTACKING_ENTITY, player).withParameter(LootContextParams.DIRECT_ATTACKING_ENTITY, player)
                .withParameter(LootContextParams.LAST_DAMAGE_PLAYER, player).create(LootContextParamSets.ENTITY);
    }
}
