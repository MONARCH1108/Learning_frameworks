import { useState } from "react";

function List() {

  const [fruits, setFruits] = useState([
    { id: 1, name: "apple", cal: 95 },
    { id: 2, name: "orange", cal: 25 },
    { id: 3, name: "banana", cal: 44 },
    { id: 4, name: "coconut", cal: 34 },
    { id: 5, name: "pineapple", cal: 64 }
  ]);

  function sortByName() {
    setFruits([...fruits].sort((a, b) =>
      a.name.localeCompare(b.name)
    ));
  }

  function sortByCal() {
    setFruits([...fruits].sort((a, b) =>
      b.cal - a.cal
    ));
  }

  return (
    <div>
      <ul>
        {fruits.map(fruit =>
          <li key={fruit.id} className="junk_food">
            {fruit.name}: <b>{fruit.cal}</b>
          </li>
        )}
      </ul>

      <button onClick={sortByName}>Sort by name</button>
      <button onClick={sortByCal}>Sort by calories</button>
    </div>
  );
}

export default List;
