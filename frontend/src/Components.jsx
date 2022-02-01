import React, { useEffect, useState } from "react";
import { Button, Card } from "react-bootstrap";
import "./Components.css";

// search results
export const EmojiCards = ({ data }) => {
  if (!data) return null;

  const copy = (text) => {
    navigator.clipboard.writeText(`:${text}:`);
  };

  const cards = data.hits.hits.map((emoji, idx) => {
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

  return (
    <div
      style={{
        display: "flex",
        flexWrap: "wrap",
        justifyContent: "center",
        marginTop: 40,
      }}
    >
      {cards}
    </div>
  );
};

// filters
export const Category = ({ category, setIdentifier }) => {
  if (!category) return null;
  // console.log(category.labels);
  return category.labels.buckets.map((label, idx) => (
    <div
      key={idx}
      style={{ margin: 12, width: "20vw" }}
      // onClick={() => setIdentifier(label.key)}
    >
      <u>{label.key}</u>
      <div>{label.doc_count}</div>
    </div>
  ));
};

// searchbar
export const Searchbar = ({ setQuery, fetchData }) => {
  return (
    <div
      style={{
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        margin: "10px 0",
      }}
    >
      <input
        name="query"
        type="search"
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
  );
};

// size per page selector
export const SizePerPage = ({ size, setSize }) => {
  const [selectedSize, setSelectedSize] = useState(size);

  const onChange = (e) => {
    setSelectedSize(e.target.value);
  };

  useEffect(() => {
    setSize(selectedSize);
  }, [selectedSize]);

  return (
    <div style={{ display: "flex" }}>
      <div style={{ marginRight: 20 }}>Cards per page</div>
      <select id="page" onChange={onChange}>
        <option value={5}>5</option>
        <option value={10}>10</option>
        <option value={15}>15</option>
      </select>
    </div>
  );
};

export const Pagination = ({ total, size, setFrom }) => {
  const MAX_DISPLAY_PAGE_COUNT = 5;
  const totalPage = Math.floor(total / size) + 1;
  const [activePage, setActivePage] = useState(1);

  useEffect(() => {
    setFrom(size * (activePage - 1));
  }, [activePage]);

  // console.log(total);
  // console.log(size);
  // console.log(totalPage);
  // console.log(activePage);

  const onClick = (e, pg) => {
    setActivePage(pg);
    return false;
  };

  // create each page link number
  const pageLinks = [];
  for (let pg = 1; pg <= totalPage; pg++) {
    if (pg < MAX_DISPLAY_PAGE_COUNT || pg === totalPage) {
      pageLinks.push(
        <a
          href="#"
          onClick={(e) => onClick(e, pg)}
          className={pg === activePage ? "active" : null}
          key={pg}
        >
          {pg}
        </a>,
      );
    }
    if (pg === MAX_DISPLAY_PAGE_COUNT) {
      pageLinks.push(
        <a href="#" id="dot" key={pg}>
          ...
        </a>,
      );
    }
  }

  return (
    <div className="pagination">
      <a
        href="#"
        onClick={(e) => onClick(e, activePage - 1)}
        className={activePage === 1 ? "disabled" : null}
      >
        &laquo;
      </a>
      {pageLinks}
      <a
        href="#"
        onClick={(e) => onClick(e, activePage + 1)}
        className={activePage === totalPage ? "disabled" : null}
      >
        &raquo;
      </a>
    </div>
  );
};
