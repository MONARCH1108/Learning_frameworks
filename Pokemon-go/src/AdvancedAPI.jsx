import { useState } from "react";

function GetDataApi() {
    const [pokemon, setPokemon] = useState("");
    const [sprite, setSprite] = useState();
    const [abilities, setAbilities] = useState([]);
    const [moves, setMoves] = useState([]);
    const [name, setName] = useState("");
    const [appSprites, SetAllSprites] = useState([]);

    const FetchData = async () => {
        const response = await fetch(`https://pokeapi.co/api/v2/pokemon/${pokemon}`);
        if (!response.ok) {
            throw new Error("Resource Not Available");
        }
        const data = await response.json();
        console.log(data)
        setSprite(data.sprites.front_default);
        setAbilities(data.abilities);
        setMoves(data.moves);
        setName(data.name);
        SetAllSprites(data.sprites);
    };

    const list_abilities = abilities.map(item => item.ability.name);
    const list_moves = moves.map(item => item.move.name);
    const all_sprites = Object.values(appSprites).filter(
        sprite => typeof sprite === "string"
    );

    return (
        <div>
            <div className="Header-field">
                <h2>Pokédex</h2>

                <input
                    type="text"
                    className="input-field"
                    placeholder="Enter pokemon Name"
                    value={pokemon}
                    onChange={(e) => setPokemon(e.target.value)}
                />

                <button className="Button-main" onClick={FetchData}>
                    Fetch Pokemon
                </button>
            </div>

            <div className="Poke-card">
                <div className="Poke-top">

                    <div className="Pokemon-basic">
                        <h2>Basic info</h2>
                        <img src={sprite} alt="Pokemon Img" id="pokemonSprite" />
                        <h2>{name}</h2>
                        <p>{list_abilities.join(", ")}</p>
                    </div>

                    {/* ✅ MOVES BOX */}
                    <div className="Pokemon-moves">
                        <ul>
                            {list_moves.map((move, index) => (
                                <li key={index}>{move}</li>
                            ))}
                        </ul>
                    </div>

                </div>

                <div className="Pokemon-sprites">
                    {all_sprites.map((spriteUrl, index) => (
                        <img
                            key={index}
                            src={spriteUrl}
                            alt="Pokemon Sprite"
                            width="96"
                        />
                    ))}
                </div>
            </div>
        </div>
    );
}

export default GetDataApi;
