import { useState } from "react";
import {
  Box,
  Button,
  Card,
  CardContent,
  Stack,
  TextField,
  Typography,
  Divider,
  Alert,
} from "@mui/material";
import LinkIcon from "../../assets/link-icon.png";
import { shortenUrl } from "../URL/url";

export default function Dashboard() {
  const [url, setUrl] = useState("");
  const [expiryDays, setExpiryDays] = useState(2);
  const [shortUrl, setShortUrl] = useState("");
  const [error, setError] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  const handleShorten = async () => {
    if (!url.trim()) {
      setError("Please enter a valid URL.");
      return;
    }

    try {
      setIsLoading(true);
      setError("");
      const response = await shortenUrl(url, expiryDays);
      setShortUrl(response.short_url);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to shorten URL.");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <Box
      component="div"
      sx={{
        minHeight: "100vh",
        bgcolor: "#f5f7fb",
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        p: 2,
      }}
    >
      <Card
        elevation={6}
        sx={{
          width: 650,
          borderRadius: 4,
        }}
      >
        <CardContent sx={{ p: 5 }}>
          <Stack component="div" spacing={3} sx={{ alignItems: "center" }}>
            <img
              src={LinkIcon}
              alt="Link Icon"
              style={{
                width: 90,
                height: 90,
              }}
            />

            <Typography component="h1" variant="h4" sx={{ fontWeight: "bold" }}>
              URL Shortener
            </Typography>

            <Typography color="text.secondary" sx={{ textAlign: "center" }}>
              Convert long URLs into short, shareable links instantly.
            </Typography>

            <Stack
              component="div"
              direction="row"
              spacing={2}
              sx={{ width: "100%" }}
            >
              <TextField
                fullWidth
                label="Enter Long URL"
                type="url"
                value={url}
                onChange={(e) => setUrl(e.target.value)}
              />

              <Button
                variant="contained"
                size="large"
                onClick={handleShorten}
                disabled={isLoading}
                sx={{
                  minWidth: 130,
                }}
              >
                {isLoading ? "Shortening..." : "Shorten"}
              </Button>
            </Stack>

            <TextField
              label="Expiry (Days)"
              type="number"
              value={expiryDays}
              onChange={(e) => setExpiryDays(Number(e.target.value))}
              sx={{
                width: 180,
              }}
            />

            {error ? <Alert severity="error">{error}</Alert> : null}

            <Divider flexItem />

            <Box component="div" sx={{ width: "100%" }}>
              <Typography
                component="h2"
                variant="subtitle1"
                sx={{ fontWeight: "bold" }}
              >
                Short URL
              </Typography>

              <Stack component="div" direction="row" spacing={2} sx={{ mt: 2 }}>
                <TextField
                  fullWidth
                  value={shortUrl}
                  placeholder="Generated short URL will appear here"
                  slotProps={{
                    input: {
                      readOnly: true,
                    },
                  }}
                />

                <Button
                  variant="outlined"
                  disabled={!shortUrl}
                  onClick={() => navigator.clipboard.writeText(shortUrl)}
                >
                  Copy
                </Button>
              </Stack>
            </Box>
          </Stack>
        </CardContent>
      </Card>
    </Box>
  );
}
