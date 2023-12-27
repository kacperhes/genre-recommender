import { Autocomplete, Box, Button, Container, TextField } from "@mui/material";
import { useEffect, useState } from "react";
import axios from "axios";

type Track = {
  name: string;
  artist: string;
  genre: string;
}

function App() {
  const [searchValues, setSearchValues] = useState<string[]>([]);
  const [genres, setGenres] = useState<string[]>([]);
  const [suggestions, setSuggestions] = useState<Track[]>([]);

  useEffect(() => {
    axios.get('http://127.0.0.1:5000/genres')
      .then(response => {
        setGenres(response.data.data);
        console.log('Genres fetched successfully');
      })
      .catch(error => {
        console.error('Error fetching genres:', error);
      });
  }, []);

  const handleSearchGenres = (_event: React.ChangeEvent<{}>, values: string[]) => {
    setSearchValues(values);
  };

  const handleSearchSuggestions = () => {
    axios.get('http://127.0.0.1:5000/suggestions', {
      params: {
        genres: searchValues.join(',')
      }
    })
      .then(response => {
        console.log('Suggestions:', response.data);
        setSuggestions(response.data.data);
        console.log(response.data.data);
      })
      .catch(error => {
        console.error('Error fetching suggestions:', error);
      });
  };


  return (
    <div className="App">
      <Container maxWidth='lg'>
        <h1>Song recommender</h1>
        <Box sx={{ mb: 4 }}>
          <Autocomplete
            freeSolo
            multiple
            id="search-autocomplete"
            options={genres}
            renderInput={(params) => (
              <TextField {...params} label="Search" variant="outlined" fullWidth />
            )}
            onChange={handleSearchGenres}
            value={searchValues}
            sx={{ mb: 2 }}
          />
          <Button variant="contained" onClick={handleSearchSuggestions}>
            Search Recommendations
          </Button>
        </Box>
        <Box>
          {suggestions.length > 0 && suggestions.map((suggestion, index) => (
            <li key={index}>
              <strong>{suggestion.name}</strong> by {suggestion.artist} ({suggestion.genre})
            </li>
          ))}
        </Box>
      </Container>
    </div>
  );
}

export default App;
