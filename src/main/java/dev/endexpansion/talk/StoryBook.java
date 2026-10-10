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
import java.util.List;
import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.resources.Identifier;
import net.minecraft.util.RandomSource;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.Items;
import org.jspecify.annotations.Nullable;

/**
 * Each people's personalities and personal stories: {@code data/endexpansion/stories/<bank>.json},
 * one book per dialogue bank. Checked by {@code tools/stories/check.py}, whose docstring is the schema.
 *
 * <p>A grown-up's story runs in chapters: they bring it up ({@code intro}), ask for a first thing
 * (requests[0]), take their time ({@code waiting}) until they are ready ({@code ready}) to tell you
 * the rest ({@code confide}), and after the other two requests let you answer it one of two ways
 * ({@code endings}); then they give you something. A child's story is one request and a gift.
 */
public final class StoryBook {
    public record Personality(String id, String label, String about, Manner manner, int weight, List<String> jobs) {}

    public record Request(String id, String title, Item item, int count, String prompt, String thanks) {}

    public record Ending(String id, String label, String text, String memory) {}

    public record Story(String id, String title, List<String> jobs, String intro, List<Request> requests, String waiting,
                        String ready, String confide, List<Ending> endings, Item gift, int giftCount) {
        /** A child's story: one request and then the gift. */
        public boolean isShort() {
            return endings.isEmpty();
        }
    }

    private static final Map<String, StoryBook> BOOKS = new ConcurrentHashMap<>();
    private static final Personality PLAIN = new Personality("steady", "Steady", "Will stand and talk for as long as you like.",
            Manner.STEADY, 1, List.of());

    private final List<String> locked;
    private final List<Personality> personalities = new ArrayList<>();
    private final List<Story> stories = new ArrayList<>();

    private StoryBook(JsonObject json) {
        this.locked = strings(json.getAsJsonArray("locked"));
        JsonArray ps = json.getAsJsonArray("personalities");
        if (ps != null) for (JsonElement el : ps) {
            JsonObject p = el.getAsJsonObject();
            personalities.add(new Personality(str(p, "id"), str(p, "label"), str(p, "about"), Manner.of(str(p, "manner")),
                    p.has("weight") ? Math.max(1, p.get("weight").getAsInt()) : 1, strings(p.getAsJsonArray("jobs"))));
        }
        JsonArray ss = json.getAsJsonArray("stories");
        if (ss != null) for (JsonElement el : ss) {
            JsonObject s = el.getAsJsonObject();
            List<Request> requests = new ArrayList<>();
            for (JsonElement r : s.getAsJsonArray("requests")) {
                JsonObject o = r.getAsJsonObject();
                requests.add(new Request(str(o, "id"), str(o, "title"), item(str(o, "item")), o.get("count").getAsInt(),
                        str(o, "prompt"), str(o, "thanks")));
            }
            List<Ending> endings = new ArrayList<>();
            JsonArray es = s.getAsJsonArray("endings");
            if (es != null) for (JsonElement e : es) {
                JsonObject o = e.getAsJsonObject();
                endings.add(new Ending(str(o, "id"), str(o, "label"), str(o, "text"), str(o, "memory")));
            }
            JsonObject gift = s.getAsJsonObject("gift");
            stories.add(new Story(str(s, "id"), str(s, "title"), strings(s.getAsJsonArray("jobs")), str(s, "intro"),
                    List.copyOf(requests), str(s, "waiting"), str(s, "ready"), str(s, "confide"), List.copyOf(endings),
                    item(str(gift, "item")), gift.get("count").getAsInt()));
        }
    }

    /** A book by bank name; a missing or broken book logs once and tells no stories. */
    public static StoryBook get(String bank) {
        return BOOKS.computeIfAbsent(bank, StoryBook::load);
    }

    private static StoryBook load(String bank) {
        String path = "/data/" + EndExpansion.MOD_ID + "/stories/" + bank + ".json";
        try (InputStream in = StoryBook.class.getResourceAsStream(path)) {
            if (in == null) {
                EndExpansion.LOG.error("Missing story book {}", path);
                return new StoryBook(new JsonObject());
            }
            return new StoryBook(JsonParser.parseReader(new InputStreamReader(in, StandardCharsets.UTF_8)).getAsJsonObject());
        } catch (Exception e) {
            EndExpansion.LOG.error("Can't read story book {}", path, e);
            return new StoryBook(new JsonObject());
        }
    }

    private static String str(JsonObject o, String key) {
        return o.has(key) ? o.get(key).getAsString() : "";
    }

    private static List<String> strings(@Nullable JsonArray array) {
        List<String> out = new ArrayList<>();
        if (array != null) for (JsonElement el : array) out.add(el.getAsString());
        return List.copyOf(out);
    }

    private static Item item(String id) {
        return id.isEmpty() ? Items.AIR : BuiltInRegistries.ITEM.getValue(Identifier.parse(id));
    }

    public List<Story> stories() {
        return stories;
    }

    public List<Personality> personalities() {
        return personalities;
    }

    /** What they say if you ask for their story before they know you. */
    public String locked(RandomSource random) {
        return locked.isEmpty() ? "Not yet." : locked.get(random.nextInt(locked.size()));
    }

    public Personality personality(String id) {
        for (Personality p : personalities) if (p.id().equals(id)) return p;
        return personalities.isEmpty() ? PLAIN : personalities.getFirst();
    }

    /** A personality for someone with this job, by weight. */
    public Personality pickPersonality(String job, RandomSource random) {
        List<Personality> fits = personalities.stream().filter(p -> p.jobs().isEmpty() || p.jobs().contains(job)).toList();
        if (fits.isEmpty()) return personalities.isEmpty() ? PLAIN : personalities.getFirst();
        int total = fits.stream().mapToInt(Personality::weight).sum(), roll = random.nextInt(total);
        for (Personality p : fits) if ((roll -= p.weight()) < 0) return p;
        return fits.getFirst();
    }

    public @Nullable Story story(String id) {
        for (Story s : stories) if (s.id().equals(id)) return s;
        return null;
    }

    /** A story for someone with this job: one of their job's own, more often than not, if it has any. */
    public @Nullable Story pickStory(String job, RandomSource random) {
        List<Story> own = stories.stream().filter(s -> s.jobs().contains(job)).toList();
        List<Story> anyone = stories.stream().filter(s -> s.jobs().isEmpty()).toList();
        if (!own.isEmpty() && (anyone.isEmpty() || random.nextInt(3) != 0)) return own.get(random.nextInt(own.size()));
        if (!anyone.isEmpty()) return anyone.get(random.nextInt(anyone.size()));
        return stories.isEmpty() ? null : stories.get(random.nextInt(stories.size()));
    }

    /** Forget loaded books (tests and resource reloads). */
    public static void clear() {
        BOOKS.clear();
    }
}
