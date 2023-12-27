import { Autocomplete, Box, Button, Container, Paper, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, TextField, Typography } from "@mui/material";
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
        <Typography variant="h3" sx={{ mb: 2 }}>
          Songs recommender
        </Typography>
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
        <Typography variant="h6" sx={{ mb: 2 }}>
          Top 25 results
        </Typography>
        <Box>
          {suggestions.length > 0 && (
            <TableContainer component={Paper}>
              <Table sx={{ minWidth: 650 }} aria-label="Suggestions table">
                <TableHead>
                  <TableRow>
                    <TableCell>#</TableCell>
                    <TableCell align="right">Song name</TableCell>
                    <TableCell align="right">Artist</TableCell>
                    <TableCell align="right">Genre</TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {suggestions.map((suggestion, index) => (
                    <TableRow 
                      key={`track-${index}`}
                      sx={{ '&:last-child td, &:last-child th': { border: 0 } }}
                    >
                      <TableCell component="th" scope="row">
                        {index + 1}
                      </TableCell>
                      <TableCell align="right">{suggestion.name}</TableCell>
                      <TableCell align="right">{suggestion.artist}</TableCell>
                      <TableCell align="right">{suggestion.genre}</TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </TableContainer>
          )}
        </Box>
      </Container>
    </div>
  );
}

export default App;
