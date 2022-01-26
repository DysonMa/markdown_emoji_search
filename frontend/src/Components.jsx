import { Button, Card, Container, Row, Col } from "react-bootstrap";

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
  console.log(category.labels);
  return category.labels.buckets.map((label, idx) => (
    <div
      key={idx}
      style={{ margin: 12 }}
      // onClick={() => setIdentifier(label.key)}
    >
      <u>
        {label.key}&nbsp;&nbsp;{label.doc_count}
      </u>
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
  );
};
