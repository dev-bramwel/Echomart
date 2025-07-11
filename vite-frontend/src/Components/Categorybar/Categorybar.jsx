//styles
import "./Categorybar.css";

// images
import electronics from "../assets/Electronics.png";
import clothes from "../assets/clothes.png";
import groceries from "../assets/groceries.png";
import bags from "../assets/bags.png";
import jewelry from "../assets/jewelry.png";
import phones from "../assets/phones.png";
import cutlery from "../assets/cutlery.png";
import art from "../assets/art.png";
import furniture from "../assets/furniture.png";

const Categorybar = () => {
  return (
    <div className="category-bar">
      <div className="category-name">
        <h1>Categories</h1>
      </div>
      <div className="category-list">
        <ul>
          <li>
            <a href="/">
              <img src={electronics} alt="Electronics" /> Electronics
            </a>
          </li>
          <li>
            <a href="/">
              <img src={clothes} alt="Clothes" /> Clothes
            </a>
          </li>
          <li>
            <a href="/">
              <img src={groceries} alt="Groceries" /> Groceries
            </a>
          </li>
          <li>
            <a href="/">
              <img src={bags} alt="Bags" /> Bags
            </a>
          </li>
          <li>
            <a href="/">
              <img src={jewelry} alt="Jewelry" /> Jewelry
            </a>
          </li>
          <li>
            <a href="/">
              <img src={phones} alt="Phones" /> Phones
            </a>
          </li>
          <li>
            <a href="/">
              <img src={cutlery} alt="Cutlery" /> Cutlery
            </a>
          </li>
          <li>
            <a href="/">
              <img src={art} alt="Art" /> Art
            </a>
          </li>
          <li>
            <a href="/">
              <img src={furniture} alt="Furniture" /> Furniture
            </a>
          </li>
        </ul>
      </div>
    </div>
  );
};

export default Categorybar;
