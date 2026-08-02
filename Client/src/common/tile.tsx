import { Card, CardContent, Typography } from "@mui/material";

// props for the MetricTile component
interface MetricTileProps {
  title: string;
  value: number | string;
}

export default function MetricTile(props: MetricTileProps) {
  return (
    <Card
      sx={{
        width: 200,
        maxWidth: 150,
        textAlign: "center",
        p: 2,
        display: "inline-block",
        margin: 1,
      }}
    >
      <CardContent>
        <Typography variant="h4" component="div" sx={{ fontWeight: "bold" }}>
          {props.value}
        </Typography>
        <Typography variant="body2" color="text.secondary">
          {props.title}
        </Typography>
      </CardContent>
    </Card>
  );
}
