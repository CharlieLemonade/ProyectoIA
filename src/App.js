import React, { useState } from "react";
import {
  Typography,
  Button,
  Box,
  TextField,
  Container,
  InputAdornment,
  Card,
  CardMedia,
  CardContent,
} from "@mui/material";
import SendIcon from "@mui/icons-material/Send";
import Slider from "react-slick";
import axios from "axios";
import "slick-carousel/slick/slick.css";
import "slick-carousel/slick/slick-theme.css";

const LocationButton = ({ text, Icon, onClick }) => (
  <Button
    variant="outlined"
    startIcon={<Icon />}
    onClick={onClick}
    sx={{
      textTransform: "none",
      color: "primary.main",
      borderColor: "primary.main",
      borderRadius: "50px",
      px: 3,
      py: 1,
      "&:hover": {
        backgroundColor: "primary.light",
        borderColor: "primary.light",
        color: "white",
      },
    }}
  >
    {text}
  </Button>
);

const FullWidthTextField = ({ onFocus, onChange }) => (
  <Box
    sx={{
      width: "100%",
      maxWidth: 700,
      mx: "auto",
      display: "flex",
      alignItems: "center",
      justifyContent: "center",
      mb: 4,
    }}
  >
    <TextField
      fullWidth
      label="Escribe tu mensaje"
      id="chatbot-input"
      variant="outlined"
      onFocus={onFocus}
      onChange={onChange}
      InputProps={{
        endAdornment: (
          <InputAdornment position="end">
            <Button
              variant="contained"
              sx={{
                backgroundColor: "primary.main",
                color: "white",
                borderRadius: "50px",
                minWidth: "40px",
                width: "40px",
                height: "40px",
              }}
            >
              <SendIcon />
            </Button>
          </InputAdornment>
        ),
      }}
      sx={{
        borderRadius: "20px",
        "& .MuiOutlinedInput-root": {
          borderRadius: "20px",
        },
      }}
    />
  </Box>
);

export default function SimplifiedComponent() {
  const [showMessage, setShowMessage] = useState(false);
  const [searchPrompt, setSearchPrompt] = useState("");
  const [recommendations, setRecommendations] = useState([]);

  const fetchRecommendations = async () => {
    try {
      const response = await axios.post("http://localhost:5000/recommend", {
        prompt: searchPrompt,
        top_n: 5,
      });
      setRecommendations(response.data);
    } catch (error) {
      console.error("Error fetching recommendations:", error);
    }
  };

  const settings = {
    dots: true,
    infinite: true,
    speed: 500,
    slidesToShow: 3,
    slidesToScroll: 1,
    responsive: [
      {
        breakpoint: 768,
        settings: {
          slidesToShow: 1,
          slidesToScroll: 1,
        },
      },
    ],
  };

  return (
    <Container>
      <Typography
        variant="h1"
        align="center"
        sx={{
          my: 4,
          textAlign: "center",
          color: "primary.main",
          fontFamily: "'Roboto', sans-serif",
          fontWeight: "bold",
        }}
      >
        GastroGuide
      </Typography>

      <FullWidthTextField
        onFocus={() => setShowMessage(true)}
        onChange={(e) => setSearchPrompt(e.target.value)}
      />

      <Box
        sx={{
          display: "flex",
          justifyContent: "center",
          gap: 2,
          mb: 4,
        }}
      >
        <LocationButton
          text="Buscar Restaurantes"
          Icon={SendIcon}
          onClick={fetchRecommendations}
        />
      </Box>

      {showMessage && (
        <Typography
          variant="h4"
          align="center"
          sx={{ color: "text.primary", mt: 2 }}
        >
          Explora opciones deliciosas
        </Typography>
      )}

      <Box sx={{ mt: 4 }}>
        <Slider {...settings}>
          {recommendations.map((item, index) => (
            <Card key={index} sx={{ maxWidth: 300, mx: "auto" }}>
              <CardMedia
                component="img"
                height="140"
                image={item.featured_image || "placeholder.jpg"}
                alt={item.name}
              />
              <CardContent>
                <Typography variant="h6" component="div">
                  {item.name}
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  {item.description || "Sin descripción disponible"}
                </Typography>
                <Typography variant="body2" color="text.primary">
                  Rating: {item.rating} ({item.reviews} reseñas)
                </Typography>
              </CardContent>
            </Card>
          ))}
        </Slider>
      </Box>
    </Container>
  );
}