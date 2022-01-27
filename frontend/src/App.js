import "./App.css";
import React, { useEffect, useState } from "react";
import axios from "axios";
import { useNavigate, useLocation } from "react-router-dom";
import {
  EmojiCards,
  Category,
  Searchbar,
  SizePerPage,
  Pagination,
} from "./Components";

function App() {
  // frontend routing
  const navigate = useNavigate();
  const location = useLocation();

  const [data, setData] = useState(null);
  const [category, setCategory] = useState(null);

  const params = new URLSearchParams(location.search);

  const [query, setQuery] = useState(params.get("query") ?? "");
  const [identifier, setIdentifier] = useState(params.get("identifier") ?? "");
  const [from, setFrom] = useState(params.get("from") ?? 0);
  const [size, setSize] = useState(params.get("size") ?? 10);

  console.log(query);
  console.log(identifier);

  const fetchData = async () => {
    // frontend routing
    const params = new URLSearchParams({ query, identifier, from, size });
    navigate(
      { pathname: location.pathname, search: params.toString() },
      { replace: true },
    );

    // fetch data
    await axios
      .post("http://localhost:5000/data", {
        query,
        identifier,
        from,
        size: !query && !identifier ? "all" : size,
      })
      .then((res) => {
        console.log(res.data);
        setData(query || identifier ? res.data : null); // must type any query or select any identifier
        setCategory(res.data.aggregations);
      })
      .catch((err) => console.error(err));
  };

  const preloadImages = () => {
    // fetch all data to preload images
    axios
      .post("http://localhost:5000/data", {
        query,
        size: "all",
      })
      .then((res) => {
        // store images to window object
        window["imgs_url"] = {};
        res.data.hits.hits?.forEach((emoji) => {
          const newImage = new Image();
          newImage.src = emoji._source.url;
          window["imgs_url"][emoji._source.name] = newImage;
        });
      })
      .catch((err) => console.error(err));
  };

  useEffect(() => {
    fetchData();
    preloadImages();
  }, []);

  useEffect(() => {
    fetchData();
  }, [size, from]);

  // useEffect(() => {
  //   console.log(identifier);
  //   // fetchData();
  // }, [identifier]);

  return (
    <div className="App">
      <header className="App-header">
        <p>Markdown Emoji Search</p>
      </header>
      <div style={{ display: "flex" /*height: "100vh"*/ }}>
        <div className="App-category">
          <h4 style={{ color: "#5f5f95" }}>Category</h4>
          <Category category={category} setIdentifier={setIdentifier} />
        </div>
        <div className="App-result">
          <Searchbar setQuery={setQuery} fetchData={fetchData} />
          <div
            style={{
              display: "flex",
              justifyContent: "space-between",
              alignItems: "center",
            }}
          >
            <Pagination
              total={data?.hits.total.value ?? 0}
              size={size}
              setFrom={setFrom}
            />
            <SizePerPage size={size} setSize={setSize} />
          </div>
          <EmojiCards data={data} />
        </div>
      </div>
    </div>
  );
}

export default App;
