import { Card, CardContent, Typography } from "@mui/material";
import { useEffect, useState } from "react";
import { getToken } from "../authProvider";

export default function Dashboard() {
  const [stats, setStats] = useState<any>(null);

  useEffect(() => {
    const load = async () => {
      const token = getToken();
      const r = await fetch("http://127.0.0.1:8000/bot/admin/stats", {
        headers: { "X-Bot-Admin-Token": token },
      });
      const j = await r.json();
      setStats(j);
    };
    load();
  }, []);

  return (
    <Card>
      <CardContent>
        <Typography variant="h5">Dashboard</Typography>
        <pre style={{ whiteSpace: "pre-wrap" }}>{stats ? JSON.stringify(stats, null, 2) : "Loading..."}</pre>
      </CardContent>
    </Card>
  );
}
