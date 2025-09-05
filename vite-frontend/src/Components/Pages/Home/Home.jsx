import React from 'react'
import "./Home.css";

const products = [
  { name: "iPhone 14 Pro Max", price: "Ksh 89,999", img: "/src/Components/Assets/products/iPhone-14-Pro-Max-Purple.jpg" },

  { name: "i8 Pro Max Watch", price: "Ksh 899", img: "/src/Components/Assets/products/i8 pro max smart watch.jpg" },

  { name: "Men Sneakers", price: "Ksh 1,299", img: "/src/Components/Assets/products/airmax-90-millitary-green.jpg" },

  { name: "Anti Blue Eye Glasses", price: "Ksh 1,900", img: "/src/Components/Assets/products/Blue Light Glasses.jpg" },

  { name: "Electric Kettle", price: "Ksh 1,499", img: "/src/Components/Assets/products/Electric Kettle.jpg" },
  
  { name: "Handbag", price: "Ksh 4,999", img: "/src/Components/Assets/products/Handbags.jpg" },
];

const Home = () => {
  return (
    <div className="whats-new">
      <div className="header">
        <h2>What's New</h2>
        <a href="/">View More</a>
      </div>
      <div className="product-grid">
        {products.map((item, i) => (
          <div className="product-card" key={i}>
            <img src={item.img} alt={item.name} />
            <p className="name">{item.name}</p>
            <p className="price">{item.price}</p>
          </div>
        ))}
      </div>
    </div>
  );
};

export default Home;

