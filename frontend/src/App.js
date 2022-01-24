import logo from "./logo.svg";
import "./App.css";
import React, { useEffect, useState } from "react";
import axios from "axios";
import { Button, Card, Container, Row, Col } from "react-bootstrap";
import { useNavigate, useLocation } from "react-router-dom";

const EmojiCards = ({ data }) => {
  if (!data) return null;

  const copy = (text) => {
    navigator.clipboard.writeText(`:${text}:`);
  };

  return data.hits.hits.map((emoji, idx) => {
    emoji = emoji._source;
    return (
      <Card style={{ width: "18rem", margin: 12 }} key={idx}>
        <Card.Img
          variant="top"
          src={window?.["imgs_url"]?.[emoji] ?? emoji.url}
        />
        <Card.Body>
          <Card.Title>
            <code>:{emoji.name}:</code>
          </Card.Title>
          <Card.Subtitle>{emoji.category}</Card.Subtitle>
          <Card.Subtitle>{emoji.sub_category}</Card.Subtitle>
          <Button variant="primary" onClick={() => copy(emoji.name)}>
            Copy
          </Button>
        </Card.Body>
      </Card>
    );
  });
};

const Category = ({ category, setFilter }) => {
  if (!category) return null;
  console.log(category);
  return category.category.buckets.map((category, idx) => (
    <div
      key={idx}
      style={{ margin: 12 }}
      onClick={() => setFilter(category.key)}
    >
      <u>
        {category.key}&nbsp;&nbsp;{category.doc_count}
      </u>
    </div>
  ));
};

function App() {
  const [data, setData] = useState(null);
  const [category, setCategory] = useState(null);
  const [filter, setFilter] = useState(null);

  const navigate = useNavigate();
  const location = useLocation();

  const params = new URLSearchParams(location.search);
  console.log(params.get("query"));
  const [query, setQuery] = useState(params.get("query") ?? "");

  const fetchData = async () => {
    // frontend routing
    const params = new URLSearchParams({ query: query });
    navigate(
      { pathname: location.pathname, search: params.toString() },
      { replace: true },
    );

    console.log(query);

    // fetch data
    await axios
      .post("http://localhost:5000/data", {
        query,
        size: query === "" ? "all" : 10,
      })
      .then((res) => {
        console.log(res.data);
        setData(query ? res.data : null);
        setCategory(res.data.aggregations);
      })
      .catch((err) => console.log(err));
  };

  const preloadImages = () => {
    // fetch all data to preload images
    axios
      .post("http://localhost:5000/data", {
        query,
        size: "all",
      })
      .then((res) => {
        console.log(res.data);
        window["imgs_url"] = {};
        res.data.hits.hits?.forEach((emoji) => {
          const newImage = new Image();
          newImage.src = emoji._source.url;
          window["imgs_url"][emoji._source.name] = newImage;
        });
        console.log(window["imgs_url"]["muscle"]);
      })
      .catch((err) => console.log(err));
  };

  useEffect(() => {
    fetchData();
    preloadImages();
  }, []);

  useEffect(() => {
    console.log("filter");
  }, [filter]);

  return (
    <div className="App">
      <header className="App-header">
        <p>Markdown Emoji Search</p>
      </header>
      <div style={{ display: "flex" /*height: "100vh"*/ }}>
        <div className="App-category">
          <h4 style={{ color: "#5f5f95" }}>Category</h4>
          <Category category={category} setFilter={setFilter} />
        </div>
        <div className="App-result">
          <div
            style={{
              display: "flex",
              justifyContent: "center",
              alignItems: "center",
            }}
          >
            <input
              name="query"
              type="text"
              onChange={(e) => {
                setQuery(e.target.value);
              }}
              onKeyDown={(e) => {
                if (e.key === "Enter") fetchData();
              }}
              style={{ margin: 12 }}
              autoComplete="off"
            />
            <Button
              variant="primary"
              as="input"
              type="button"
              value="Search"
              onClick={fetchData}
            />
          </div>
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
        </div>
      </div>
    </div>
  );
}

export default App;
