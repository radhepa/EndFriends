package dev.endexpansion;

import net.fabricmc.fabric.api.creativetab.v1.CreativeModeTabEvents;
import net.minecraft.core.Registry;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.core.registries.Registries;
import net.minecraft.resources.ResourceKey;
import net.minecraft.world.item.CreativeModeTabs;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.Rarity;

/**
 * Enderman Eyes: a pair of preserved royal eyes in an obsidian reliquary, the seal of a Court envoy.
 * Carry them into a Citadel and you are a guest; lose them there and you are not. They lie on one
 * End ship in five ({@code mixin/EndShipEyesMixin}).
 */
public final class EndItems {
    private EndItems() {}

    public static final Item ENDERMAN_EYES = register("enderman_eyes",
            new Item.Properties().stacksTo(1).rarity(Rarity.EPIC).fireResistant());

    private static Item register(String name, Item.Properties properties) {
        ResourceKey<Item> key = ResourceKey.create(Registries.ITEM, EndExpansion.id(name));
        return Registry.register(BuiltInRegistries.ITEM, key, new Item(properties.setId(key)));
    }

    public static void register() {
        CreativeModeTabEvents.modifyOutputEvent(CreativeModeTabs.INGREDIENTS).register(out -> out.accept(ENDERMAN_EYES));
    }
}
