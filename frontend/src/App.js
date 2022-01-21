import logo from "./logo.svg";
import "./App.css";
import React, { useEffect, useState } from "react";
import axios from "axios";
import { Button, Card, Container, Row, Col } from "react-bootstrap";
import { useNavigate, useLocation } from "react-router-dom";

const EmojiCards = ({ data }) => {
  if (!data) return null;
  return data.map((emoji, idx) => {
    emoji = emoji._source;
    return (
      <Card style={{ width: "18rem" }} key={idx}>
        <Card.Img variant="top" src={emoji.url} />
        <Card.Body>
          <Card.Title>{emoji.name}</Card.Title>
          <Card.Subtitle>{emoji.category}</Card.Subtitle>
          <Card.Subtitle>{emoji.sub_category}</Card.Subtitle>
          {/* <Card.Text>
        Some quick example text to build on the card title and make up the bulk of
        the card's content.
      </Card.Text> */}
          <Button variant="primary">Go somewhere</Button>
        </Card.Body>
      </Card>
    );
  });
};

function App() {
  const [data, setData] = useState(null);

  const navigate = useNavigate();
  const location = useLocation();

  const params = new URLSearchParams(location.search);
  const [query, setQuery] = useState(params.get("query"));

  const fetchData = () => {
    // frontend routing
    const params = new URLSearchParams({ query: query });
    navigate(
      { pathname: location.pathname, search: params.toString() },
      { replace: true },
    );

    // fetch data
    axios
      .post("http://localhost:5000/data", {
        query: query,
      })
      .then((res) => {
        console.log(res.data);
        setData(res.data);
      })
      .catch((err) => console.log(err));
  };

  useEffect(() => {
    fetchData();
  }, []);

  return (
    <div className="App">
      <header className="App-header">
        {/* <img src={logo} className="App-logo" alt="logo" /> */}
        <p>Markdown Emoji Search</p>
        {/* <a
          className="App-link"
          href="https://reactjs.org"
          target="_blank"
          rel="noopener noreferrer"
        >
          {message?.data ?? "none"}
        </a> */}
        <input
          name="query"
          type="text"
          onChange={(e) => {
            setQuery(e.target.value);
          }}
          onKeyDown={(e) => {
            if (e.key === "Enter") fetchData();
          }}
        />
        <Button
          variant="primary"
          as="input"
          type="button"
          value="Search"
          onClick={fetchData}
        />
        <div
          style={{
            display: "flex",
            flexWrap: "wrap",
            justifyContent: "center",
            marginTop: 40,
          }}
        >
          <EmojiCards data={data} />
        </div>
      </header>
    </div>
  );
}

export default App;
