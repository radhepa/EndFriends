package dev.endexpansion.talk;

import com.google.gson.JsonArray;
import com.google.gson.JsonElement;
import com.google.gson.JsonObject;
import com.google.gson.JsonParser;
import dev.endexpansion.EndExpansion;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.nio.charset.StandardCharsets;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.NavigableMap;
import java.util.TreeMap;
import java.util.concurrent.ConcurrentHashMap;
import java.util.regex.Matcher;
import java.util.regex.Pattern;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.util.RandomSource;
import net.minecraft.world.item.ItemStack;
import org.jspecify.annotations.Nullable;

/**
 * Everything the End peoples can say: {@code data/endexpansion/dialogue/<bank>.json}, one bank per
 * voice (shulkin, chorrin, their children, the court). Checked by {@code tools/dialogue/check.py}.
 *
 * <p>Every topic maps minimum levels (0-10) to lines; for level L the lines under the largest key
 * at or below L are used, so what a resident says changes as they come to know you. Court ranks and
 * folk jobs can override a topic.
 */
public final class DialogueBank {
    private static final Map<String, DialogueBank> BANKS = new ConcurrentHashMap<>();
    private static final Pattern PLACEHOLDER = Pattern.compile("\\{([a-z]+)}");
    private static final DialogueBank EMPTY = new DialogueBank("empty", new JsonObject());

    private final String name;
    private final Map<String, NavigableMap<Integer, List<String>>> topics = new HashMap<>();
    private final Map<String, NavigableMap<Integer, List<String>>> jobs = new HashMap<>();
    private final Map<String, Map<String, NavigableMap<Integer, List<String>>>> ranks = new HashMap<>();
    private final List<String> levels, names, places;
    private final Map<String, String> tastes = new HashMap<>();

    private DialogueBank(String name, JsonObject json) {
        this.name = name;
        this.levels = strings(json.getAsJsonArray("levels"));
        this.names = strings(json.getAsJsonArray("names"));
        this.places = strings(json.getAsJsonArray("places"));
        tables(json.getAsJsonObject("topics"), topics);
        tables(json.getAsJsonObject("jobs"), jobs);
        JsonObject r = json.getAsJsonObject("ranks");
        if (r != null) for (var e : r.entrySet()) {
            Map<String, NavigableMap<Integer, List<String>>> rank = new HashMap<>();
            tables(e.getValue().getAsJsonObject(), rank);
            ranks.put(e.getKey(), rank);
        }
        JsonObject gifts = json.getAsJsonObject("gifts");
        if (gifts != null) for (var e : gifts.entrySet()) {
            for (String id : strings(e.getValue().getAsJsonArray())) tastes.put(id.contains(":") ? id : "minecraft:" + id, e.getKey());
        }
    }

    /** A bank by name; a missing or broken bank logs once and says nothing (the game keeps running). */
    public static DialogueBank get(String name) {
        return BANKS.computeIfAbsent(name, DialogueBank::load);
    }

    private static DialogueBank load(String name) {
        String path = "/data/" + EndExpansion.MOD_ID + "/dialogue/" + name + ".json";
        try (InputStream in = DialogueBank.class.getResourceAsStream(path)) {
            if (in == null) {
                EndExpansion.LOG.error("Missing dialogue bank {}", path);
                return EMPTY;
            }
            return new DialogueBank(name, JsonParser.parseReader(new InputStreamReader(in, StandardCharsets.UTF_8)).getAsJsonObject());
        } catch (Exception e) {
            EndExpansion.LOG.error("Can't read dialogue bank {}", path, e);
            return EMPTY;
        }
    }

    private static void tables(@Nullable JsonObject json, Map<String, NavigableMap<Integer, List<String>>> into) {
        if (json == null) return;
        for (var e : json.entrySet()) {
            NavigableMap<Integer, List<String>> table = new TreeMap<>();
            for (var level : e.getValue().getAsJsonObject().entrySet()) {
                table.put(Integer.parseInt(level.getKey()), strings(level.getValue().getAsJsonArray()));
            }
            into.put(e.getKey(), table);
        }
    }

    private static List<String> strings(@Nullable JsonArray array) {
        List<String> out = new ArrayList<>();
        if (array != null) for (JsonElement el : array) out.add(el.getAsString());
        return List.copyOf(out);
    }

    public String name() {
        return name;
    }

    /** Level names (0-10); children's banks use their people's. */
    public String levelName(int level) {
        if (levels.isEmpty() && name.endsWith("_child")) return get(name.substring(0, name.length() - 6)).levelName(level);
        return levels.isEmpty() ? "Level " + level : levels.get(Math.clamp(level, 0, levels.size() - 1));
    }

    public List<String> names() {
        if (names.isEmpty() && name.endsWith("_child")) return get(name.substring(0, name.length() - 6)).names();
        return names;
    }

    public List<String> places() {
        return places;
    }

    public boolean has(String topic) {
        return topics.containsKey(topic);
    }

    /** How the bank's people feel about an item: loved, liked, disliked or neutral. */
    public String taste(ItemStack stack) {
        return tastes.getOrDefault(BuiltInRegistries.ITEM.getKey(stack.getItem()).toString(), "neutral");
    }

    /**
     * A line on a topic at this level: the rank's own lines first (Court), then the job's (for the
     * "work" topic), then the shared ones. Tries not to repeat {@code avoid}. Null if there is none.
     */
    public @Nullable String pick(String topic, int level, @Nullable String rank, @Nullable String job, RandomSource random, @Nullable String avoid) {
        List<String> pool = null;
        if (rank != null && ranks.containsKey(rank)) pool = pool(ranks.get(rank).get(topic), level);
        if (pool == null && job != null && topic.equals("work")) pool = pool(jobs.get(job), level);
        if (pool == null) pool = pool(topics.get(topic), level);
        if (pool == null || pool.isEmpty()) return null;
        String line = pool.get(random.nextInt(pool.size()));
        if (line.equals(avoid) && pool.size() > 1) line = pool.get((pool.indexOf(line) + 1 + random.nextInt(pool.size() - 1)) % pool.size());
        return line;
    }

    private static @Nullable List<String> pool(@Nullable NavigableMap<Integer, List<String>> table, int level) {
        if (table == null) return null;
        var entry = table.floorEntry(level);
        return entry == null ? table.firstEntry().getValue() : entry.getValue();
    }

    /** Fills {placeholders} from {@code vars}; unknown ones are left as they are. */
    public static String fill(String line, Map<String, String> vars) {
        Matcher m = PLACEHOLDER.matcher(line);
        StringBuilder out = new StringBuilder();
        while (m.find()) m.appendReplacement(out, Matcher.quoteReplacement(vars.getOrDefault(m.group(1), m.group(0))));
        m.appendTail(out);
        return out.toString();
    }

    /** Forget loaded banks (tests and resource reloads). */
    public static void clear() {
        BANKS.clear();
    }
}
