import { Card, CardContent, Button, Stack, Typography } from "@mui/material";
import { getToken } from "../authProvider";

async function cleanup(params: string) {
  const token = getToken();
  const r = await fetch(`http://127.0.0.1:8000/bot/admin/orders/cleanup?${params}`, {
    method: "DELETE",
    headers: { "X-Bot-Admin-Token": token },
  });
  return r.json();
}

export default function Cleanup() {
  return (
    <Card>
      <CardContent>
        <Typography variant="h5">Cleanup</Typography>
        <Stack spacing={2} direction="row" sx={{ mt: 2, flexWrap: "wrap" }}>
          <Button variant="contained" onClick={async () => alert(JSON.stringify(await cleanup("status=closed")))}>
            Delete closed
          </Button>
          <Button variant="contained" onClick={async () => alert(JSON.stringify(await cleanup("status=rejected")))}>
            Delete rejected
          </Button>
          <Button variant="outlined" onClick={async () => alert(JSON.stringify(await cleanup("older_than_days=30")))}>
            Delete older than 30d
          </Button>
        </Stack>
      </CardContent>
    </Card>
  );
}
