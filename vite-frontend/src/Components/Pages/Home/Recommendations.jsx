import React from 'react'

import "./Recommendations.css";

const recommended = [
  { name: "Men’s Sneakers (Size 39-45)", price: "Ksh 4,500", rating: 1325, img: "/src/Components/Assets/products/airmax-90-millitary-green.jpg" },

  { name: "Women's Leather Handbag", price: "Ksh 6,900", rating: 4875, img: "/src/Components/Assets/products/Handbags.jpg" },

  { name: "Z9 Bluetooth Earphone", price: "Ksh 899", rating: 2154, img: "src/Components/Assets/Products/Wireless BT Earbuds.jpg" },

  { name: "Apple MacBook Air M4", price: "Ksh 120,000", rating: 1985, img: "/src/Components/Assets/products/apple-m4-macbook-pro.jpg" },

  { name: "Fresh Sweet Strawberries", price: "Ksh 500", rating: 5971, img: "src/Components/Assets/Products/Fresh Sweet Strawberries.jpg"},
];

const Recommendations = () => {
  return (
    <div className="recommendations">
      <h2>You May Also Like</h2>
      <div className="recommend-grid">
        {recommended.map((item, i) => (
          <div className="recommend-card" key={i}>
            <img src={item.img} alt={item.name} />
            <p className="name">{item.name}</p>
            <p className="price">{item.price}</p>
            <p className="rating">⭐ {item.rating.toLocaleString()}</p>
          </div>
        ))}
      </div>
      <div className="show-more">
        <button>SHOW MORE</button>
      </div>
    </div>
  );
};

export default Recommendations;

