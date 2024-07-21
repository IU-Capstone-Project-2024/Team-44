from fastembed import SparseTextEmbedding
from typing import List, Dict, Any

from .Embedder import Embedder

from qdrant_client import QdrantClient, models
import os
from dotenv import load_dotenv

load_dotenv()
base_collection_name = os.getenv("COLLECTION")


class VectorStore:
    def __init__(self, url: str = "http://qdrant:6333") -> None:
        self.client = QdrantClient(
            url=url,
            prefer_grpc=True,
        )

        self.model_bm42 = SparseTextEmbedding(
            model_name="Qdrant/bm42-all-minilm-l6-v2-attentions"
        )
        self.model_nomic = Embedder()

        self.create_collection(collection_name=base_collection_name, dist="eucliad")

    def __initialize_collection(self, collection_name: str, dist: str = "cosine"):
        if not self.client.collection_exists(collection_name=collection_name):
            print("Creating collection")
            dist_ = (
                models.Distance.COSINE if dist == "cosine" else models.Distance.EUCLID
            )
            self.client.create_collection(
                collection_name=collection_name,
                vectors_config={
                    "nomic": models.VectorParams(
                        size=self.model_nomic.embedding_size,
                        distance=dist_,
                        hnsw_config=models.HnswConfigDiff(
                            m=64,
                            ef_construct=526,
                            on_disk=False,
                        ),
                        on_disk=False,
                    )
                },
                sparse_vectors_config={
                    "bm42": models.SparseVectorParams(
                        modifier=models.Modifier.IDF,
                        index=models.SparseIndexParams(
                            on_disk=False,
                        ),
                    )
                },
                hnsw_config=models.HnswConfigDiff(
                    m=64,
                    ef_construct=526,
                ),
            )
            return True
        return False

    def create_collection(self, collection_name: str, dist: str) -> bool:
        assert type(collection_name) == str
        assert dist in ["cosine", "eucliad"]

        return self.__initialize_collection(collection_name, dist)

    def __add(
        self,
        chunks: List[str],
        idx: List[str | int],
        metadata: List[Dict],
        collection_name: str,
        **kwargs: Any,
    ) -> None:
        vectors = {
            "nomic": [chunk for chunk in self.model_nomic.embed_query(chunks)],
            "bm42": list(self.model_bm42.query_embed(chunks)),
        }
        self.client.upsert(
            collection_name=collection_name,
            points=[
                models.PointStruct(
                    id=id,
                    payload=payload,
                    vector={
                        "nomic": dense,
                        "bm42": models.SparseVector(
                            values=sparse.values,
                            indices=sparse.indices,
                        ),
                    },
                )
                for id, payload, dense, sparse in zip(
                    idx, metadata, vectors["nomic"], vectors["bm42"]
                )
            ],
        )

    def add(
        self,
        collection_name: str,
        **kwargs: Any,
    ) -> None:
        self.__add(collection_name=collection_name, **kwargs)

    def __search_both(self, collection_name: str, query: str, top: int = 5):
        sparse_embedding = list(self.model_bm42.query_embed(query))[0]
        dense_embedding = list(self.model_nomic.embed_query(query))

        return self.client.query_points(
            collection_name=collection_name,
            prefetch=[
                models.Prefetch(
                    query=sparse_embedding.as_object(),
                    using="bm42",
                    limit=top * 2,
                ),
                models.Prefetch(
                    query=dense_embedding,
                    using="nomic",
                    limit=top * 2,
                ),
            ],
            query=models.FusionQuery(fusion=models.Fusion.RRF),
            limit=top,
        )

    def search(self, collection_name: str, query: str, **kwargs: Any) -> List[Any]:
        return self.__search_both(
            collection_name=collection_name, query=query, **kwargs
        )


if __name__ == "__main__":
    import semantic_chunkers

    text_giant = """
World
Roshar is the native name for the planet on which The Stormlight Archive is set. It is also the name of the supercontinent on which the main events of the series take place. The planet was settled by the two Shards Honor and Cultivation, while their rival Odium exercises his influence on the planet. [46] People from Roshar are called Rosharans.[47] Roshar is the second planet from its sun and has three moons, each of which waxes and wanes separately from the others.[48] The world is regularly assaulted by Highstorms, storms characterized by a very violent storm front traveling from east to west (beginning at the Origin), followed by weaker rains. The lands in Shinovar, farthest west on the main continent of Roshar, are mostly protected from the Highstorms by the high peaks of the Misted Mountains. Most plants that grow in Shinovar, which resemble real-world plant life, cannot grow in other parts of Roshar. Highstorms come frequently and, though they do not appear to follow a simple pattern, storm wardens are able to accurately predict their schedule through complex mathematics. Flora and fauna have evolved to cope with this condition.[49]

Nations and regions:
During the Heraldic Epochs, Roshar was ruled by a coalition of ten nations known as the Silver Kingdoms. In the Era of Solitude, following the departure of the Heralds and the demise of the Orders of Knights Radiant, those kingdoms split into smaller ones, some of the more important being:
Alethkar
Jah Keved
Herdaz
Thaylenah
Kharbranth and Natani cities in the Frostlands
Numerous Makabaki countries, with Azir being most prominent
Shinovar
Rira and Iri

Races:
The Stormlight Archive features several different races, the majority of which are different ethnicities of human or partly human. Some of these races include:
Thaylens: Renowned traders and merchants native to an island nation. They possess long eyebrows that can be styled to either droop or curve behind their ears.
Alethi: Native to the nation of Alethkar, the Alethi are members of one of the four Vorin nations. They have a famed military heritage and are possessed of tan skin and dark hair.
Veden: Native to the Vorin nation of Jah Keved, the Vedens are characterized by pale skin and black hair. Some have red hair, indicating Unkalaki ancestry.
Natan: Native to the Vorin nation inhabiting New Natanan, the Natan often wear gloves and have faintly bluish skin.
Unkalaki (Horneaters): A relatively rare race, the Horneaters are called thus by other races because the Unkalaki consider animal horns, shells, and claws to be a delicacy. They possess reddish hair and dark skin, and stand well over seven feet (2.1 m) tall. The Unkalaki homeland is in the mountains of Jah Keved. Their culture is very different from the other Vorin cultures.
Parshendi (Singers/Listeners): A proud nonhuman race, living on Shattered Plains with a strong warrior culture. The Parshendi are viewed by many other races as savages because of their culture and past deeds. They have marbled red and white or red and black skin that forms patterns unique to each individual and an exoskeleton that acts as natural armor. They are at war with the Alethi during the novels' main timeline. They use spren to morph into many different forms, each with a unique function and set of abilities. These forms also change the appearance of the Parshendi who use them, for example taking warform makes them more physically able and grants them the mindset of a soldier. The workform allows them to be sturdier to perform physical labor. They also communicate through songs and rhythms in their heads. At the start of the series, many members of this species are found in a mentally limited form known as Parshmen, who are enslaved by various human groups.
Shin: A race native to the region of Shinovar, Shin have white skin and lack epicanthic folds (unlike the other races). They stand shorter than most others, averaging five feet tall. They also have bigger and rounder eyes.
Makabaki: Native to the nation of Azir and neighboring countries, Makabaki have dark skin and hair.
Dysian Aimians: otherwise known as the Sleepless. A non-human race native to Aimia, but of otherworldly origin. They are made of many small creatures with exoskeletons called hordelings. There are 24 known Sleepless on Roshar.
Siah Aimians: a non-human race also native to Aimia. They are characterized as having white-blue skin and shadows that point the wrong way. They can also change their bodies slightly, for example adding a tattoo mentally, or removing their sense of smell.

Class structure:
Much of The Way of Kings takes place within the nations of Alethkar and Jah Keved. Both of these nations divide their people into classes, primarily based on the color of their eyes. Those with dark eye colors (brown, dark green, charcoal grey) are mostly peasants (and can even be made slaves). Those with light eye colors (blue, yellow, tan, green, violet, orange, etc.) are the nobles and generally more educated ruling class. Within these classes, there are further class distinctions known as nahn (for darkeyes) and dahn (for lighteyes). Both have ten levels within. For the nahn, they range from slaves in the 10th nahn to full citizens with the right to travel in the second and first nahn. In the dahn system, lighteyes in the 10th dahn are considered only slightly better than darkeyes, and a very rich darkeyed man or woman may marry into an extremely poor lighteyed family, in very rare cases. The first dahn is composed of the king alone. It has been known for dark eyed individuals to obtain light eyes through obtaining Shardblades, a supernatural weapon in this world; however, this is exceptionally rare.

Spren:
Spren are spirits in the land of Roshar which are drawn to different conditions or emotions. There are thousands of varieties. One character, Hesina, the mother of Kaladin states, "Spren appear when something changes - when fear appears, or when it begins to rain. They are the heart of change, and therefore the heart of all things."[50] Their intelligence varies, with Cryptics (also known as liespren though they themselves dislike the term) and honorspren among the most intelligent, and more common spren, seen as forces of nature/emotion having little to no intelligence. Jasnah Kholin also mentions that the 10 orders of the Knights Radiant drew their power from spren. Some notable spren are Syl, an Honorspren who shares a bond with Kaladin, giving him surgebinding powers of Windrunner; Pattern, a Cryptic who created a bond with Shallan, allowing her to surgebind; and the cultivationspren Wyndle, who bonded with the thief Lift, allowing her to surgebind. Dalinar Kholin also bonds a spren, the Stormfather, though he does so in an unconventional manner. Jasnah bonded an inkspren named Ivory.
Some spren, such as flamespren, share characteristics with current observations in quantum mechanics, and are based on them.[51] For example, when they are observed they remain stable in the recorded state, but when tested more thoroughly, they change as though at random.
As revealed in the second book, Spren are "concepts and ideas" given physical form by the human collective subconscious. Among the many forms of spren, some are intelligent, possess self-awareness, and have even built their own cities. They reside naturally in Shadesmar, and often cross over into the physical realm. This comes at the cost of most of their self-awareness for the higher, more exalted spren, which they can regain by making bonds with humans. The sea and land are reversed in Shadesmar—what would be land on Roshar is a sea of black beads in Shadesmar, each representing a physical form on Roshar. Shadesmar also contains cities and a strange type of flora.

Religion:
Much of the world follows the Vorin religion. Vorinism tells of a struggle between forces of the Voidbringers and humanity. The Voidbringers forced humanity out of its afterlife, called the Tranquiline Halls. They believe that upon death the soul continues in its past role, but towards the regaining of the Tranquiline Halls. In Alethkar, a man's highest calling is as a warrior in life to remain a warrior in the afterlife. The religion also tells of the Lost Radiants, an order who once fought against the Voidbringers during the wars against them on Roshar (known as Desolations). Vorinism gave the Knights Radiant the moniker "Lost Radiants" after they apparently betrayed humanity at some point in the distant past. Vorinism is arranged in devotaries, whose ardents aim to assist people in advancing their Callings, which are tasks to which one dedicates their life as a method of worship. Each person selects a devotary based on variances in beliefs, talents or personality traits, and may change their selection at any point in their life. Some examples are the Devotary of Sincerity, who are encouraged to learn and ask questions, and the Devotary of Denial. Adolin Kholin's calling, for example, is Dueling. The priesthood of the Vorin religion are referred to as ardents.
Those who reject the existence of the Almighty, such as Jasnah Kholin, are referred to as heretics. Followers of other religions mentioned in The Way of Kings are Stone Shamans, Ysperists and Maakians.

Shardblades and Shardplate:
Shardblades are powerful swords that have the ability to cut through any non-living matter with ease. When used on living creatures, they can kill or maim with a single cut by the blade passing through the living soul. They can also render limbs useless when they cut through them. The only known defenses against a Shardblade are Shardplate, shields called "half-shards", another Shardblade, or an aluminum blade (according to "Rhythm of War"). Those who own a Shardblade can summon their blade from thin air in ten heartbeats and can make their blade disappear at will.[52] The blades are rare and highly valued, and there are estimated to be fewer than one hundred known blades in the world.[53]
Shardplate is full plate armor that both protects and strengthens the wearer. The armor provides protection against Surgebinding, as one wearing the armor cannot be "lashed" directly.[54] Repeated strikes at the same spot on the armor by regular weapons or Shardblades can cause the armor to crack and break. The armor can be repaired or "regrown", though it takes a long time.[55]
A full shardbearer, one wielding both Shardblade and Shardplate, is a force capable of turning the tide of battle on its own. Kaladin and Syl express a revulsion to the Shardblades wielded by the Alethi. During Dalinar's visions, he sees the Knights Radiant wearing Shardplate and wielding Shardblades, but he notes that the plate when worn by the Radiants glows. Additionally, the number of Blades and Plate worn by the Radiants is much greater than the number left in the world at the main timeline of The Way of Kings. Most Shardblades are actually dead spren that come alive for a period of time by attuning themselves to their owner's heartbeat.[56]
Shardblades wielded by the Knights Radiant are the Knight's spren taking the physical form of a weapon (often a sword, but can take the form of any weapon or a shield). Hence, these Shardblades are a physical manifestation of a living spren. 'Living' Shardblades can be summoned instantly, and do not require the summoning period of ten heartbeats. There are also ten Honorblades that grant the powers of one order of Radiants. These weapons don't appear to be physical manifestations of spren, dead or alive, and were wielded by The Heralds until nine of them were abandoned at the end of Aharietiam, or the last desolation. Szeth, the assassin in white, uses an Honorblade of Jezrien in the first two books, and the Herald, Nalan, wields the Honorblade of the Skybreakers.

Magic:
Surgebinding
Surgebinding refers to a group of ten magic systems that stem from Honor and Cultivation, two of the three Shards of Adonalsium present on Roshar. Each of Surgebinding's ten systems revolves around 'binding' two natural 'Surges,' for instance Gravity and Adhesion, to the Surgebinder's will. Surgebinding is powered by Stormlight, and the ability is granted to humans through bonding with a Spren, a type of elemental spirit native to Roshar. There are ten Surgebinding's branches, with Windrunning and powers of Lightweavers (Transformation - Soulcasting and Illumination - illusions), described most thoroughly.
Windrunning is an ability where the wielder uses the power of Stormlight to affect gravity and adhesion. It is described in three methods known as the "Three Lashings". A Basic Lashing changes the direction of gravitational pull for an individual (causing the person to be pulled towards another object or direction instead of towards the center of the planet). A Full Lashing is described as creating an almost[57] unbreakable bond between two objects until the Stormlight dissipates. A Reverse Lashing causes an object to have a much stronger gravitational pull, causing other objects to be pulled towards it.[57]
The Knights Radiant
The Knights Radiant originated through spren copying the abilities which the Heralds obtained through their Honorblades. The Knights Radiant gained power through spren by creating a bond with them called the Nahel bond. The bond gives the spren sentience while giving the human Surgebinding abilities. Two examples are Sylphrena, an Honorspren, who shares a bond with Kaladin, giving him the power to Surgebind; and Pattern, a Liespren (Cryptic), who shares a bond with Shallan, granting her power to Soulcast and create Illusions.
The Knights Radiant lived by their order's Five Ideals, called The Immortal Words, with the First Ideal being the same for every order: Life before death, strength before weakness, journey before destination. The other four Ideals are different for each order, with the exception of the Order of the Lightweavers, having only the First Ideal. Lightweavers instead must admit truths to themselves in order to progress. Towards the end of The Way of Kings, Kaladin utters the Second Ideal for the Order of Windrunners: I will protect those who cannot protect themselves. Near the end of Words of Radiance, Kaladin whispers the Third Ideal for the Order of Windrunners: I will protect even those I hate, so long as it is right. At the climax of “Rhythm of War,” he speaks the Fourth Ideal: I accept that there will be those I cannot protect.
Orders of the Knights Radiant
Windrunners: Manipulate the Surges of Adhesion and Gravitation. Bonded to Honorspren.
Skybreakers: Manipulate the Surges of Gravitation and Division. Bonded to Highspren.
Dustbringers: Manipulate the Surges of Division and Abrasion. Bonded to Ashspren.
Edgedancers: Manipulate the Surges of Abrasion and Progression. Bonded to Cultivationspren.
Truthwatchers: Manipulate the Surges of Progression and Illumination. Bonded to Mistspren.
Lightweavers: Manipulate the Surges of Illumination and Transformation. Bonded to Liespren (Cryptic).
Elsecallers: Manipulate the Surges of Transformation and Transportation. Bonded to Inkspren.
Willshapers: Manipulate the Surges of Transportation and Cohesion. Bonded to Lightspren (Reachers).
Stonewards: Manipulate the Surges of Cohesion and Tension. Bonded to Peakspren.
Bondsmiths: Manipulate the Surges of Tension and Adhesion. Bonded to three unique spren (the Nightwatcher, the Stormfather, and the Sibling). Therefore, there can only be three Bondsmiths.[58]

Soulcasting and Shadesmar:
Soulcasting is a practice where objects are changed from one form to another. It has proven able to turn rock into smoke, purify blood of poisons, and create food, among many other applications. Soulcasting is done by means of a device called a soulcaster that is powered by gems imbued with Stormlight. The type of gem placed inside the soulcaster determines what the caster can transform. With each use of a soulcaster, there is a chance of the gem cracking and being destroyed, especially when a large amount of matter is changed.[59] The main practitioners of soulcasting are the Ardents of the Vorin religion, however, there are a few exceptions. Shallan's father's steward knew how to use a soulcaster,[60] as he used Shallan's father's soulcaster.
By the end of The Way of Kings, Jasnah Kholin and Shallan are capable of doing magic that has very similar effects to Soulcasting but does not require a soulcaster to be used, and does not require that the magic user is in physical contact with the object they transform.[61] This book does not go into great detail, but the magic involves mentally communicating with an unknown source to enter a place called Shadesmar. Shadesmar is described in detail in the book but mostly consists of a world made from tiny glass beads. Once within Shadesmar, the power from a Stormlight-infused gem can be used to manipulate objects.[62]
In an interview with Brandon Sanderson, Shadesmar is described as a Cognitive Realm connecting all the worlds in the Cosmere. Sanderson has confirmed that Hoid is very good at using Shadesmar, that this is how Hoid moves between worlds, and that people on other worlds within the Cosmere have ways of accessing Shadesmar which are different from those the characters in this book use.[63]

Voidbinding:
Similar to Surgebinding, Voidbinding has a collection of surges that the third god of Roshar, Odium, makes available to his selected servants, called Fused. Unlike Knights Radiant, each Fused can only access a single surge, from a list of nine: Gravitation, Division, Abrasion, Progression, Illumination, Transformation, Transportation, Cohesion, and Tension. Adhesion is considered to be exclusive to Honor by the Fused, who cannot access it.
Voidbinding includes various other types of magic associated with Odium, such as some of the forms that Parshendi/Singers can take on that align them to Odium's ideals.

Old Magic:
Very little is known about the Old Magic, a set of powers exclusive to the goddess Cultivation. Its most common effects are those granted by her powerful spren, the Nightwatcher, who will grant boons and curses to supplicants who come to her for assistance; any boon granted is offset by a mandatory applied curse. Supplicants will often find that a boon is not granted as they expected it to, as the Nightwatcher does not always understand human desires and customs; poorly-worded requests can have unsatisfactory results. The curses applied can be anywhere from mild to fully debilitating.
"""

    text_splitter = semantic_chunkers.StatisticalChunker(
        encoder=Embedder(),
        name="statistical_chunker",
        threshold_adjustment=0.01,
        dynamic_threshold=True,
        window_size=5,
        min_split_tokens=100,
        max_split_tokens=500,
        split_tokens_tolerance=10,
        plot_chunks=False,
        enable_statistics=False,
    )
    # IDEALLY NOT TOO SMALL TEXT
    chunks_sp = text_splitter(docs=[text_giant])[0]
    chunks = [" ".join(chunk.splits) for chunk in chunks_sp]
    meta = [
        {
            "Payload": {
                "tokens": chunk.token_count,
                "triggered_score": chunk.triggered_score,
                "text": " ".join(chunk.splits),
            }
        }
        for chunk in chunks_sp
    ]
    idx = [
        i for i in range(len(chunks))
    ]  # SHOULD BE UNIQUE OR DATABASE RECREATE NEW POINT INSTEAD OF OLD ONES

    database = VectorStore()
    cool_name = "Some+cool_collection"

    database.create_collection(collection_name=cool_name, dist="cosine")
    database.add(
        chunks=chunks,
        idx=[i for i in range(len(chunks))],  # !!!! SHOULD BE UNIQUE
        metadata=meta,
        collection_name=cool_name,
    )
    results = database.search(
        collection_name=cool_name,
        query="High Storm",
    )
    print(results)
    database.client.delete_collection(collection_name=cool_name)
