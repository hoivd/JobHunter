// backend/server.js
import express from 'express';
import neo4j from 'neo4j-driver';
import cors from 'cors';

const app = express();
app.use(cors());
const port = 5000;

// Kết nối Neo4j Aura
const driver = neo4j.driver(
  'neo4j+s://122aaf61.databases.neo4j.io',
  neo4j.auth.basic('122aaf61', '_rjltNlSSQQT2aVmXOscfS7KnJm8GoIWKSEPlrTkPOM')
);

app.get('/api/graph', async (req, res) => {
  const session = driver.session();
  try {
    const result = await session.run('MATCH (n)-[r]->(m) RETURN n,r,m LIMIT 100');
    const nodes = [];
    const links = [];

    result.records.forEach(record => {
      const n = record.get('n');
      const m = record.get('m');
      const r = record.get('r');

      nodes.push({ id: n.identity.toString(), label: n.properties.name || n.labels[0] });
      nodes.push({ id: m.identity.toString(), label: m.properties.name || m.labels[0] });
      links.push({ source: n.identity.toString(), target: m.identity.toString(), type: r.type });
    });

    const uniqueNodes = Array.from(new Map(nodes.map(n => [n.id, n])).values());
    res.json({ nodes: uniqueNodes, links });
  } catch (err) {
    console.error(err);
    res.status(500).send('Error fetching graph');
  } finally {
    await session.close();
  }
});

app.listen(port, () => console.log(`Backend running at http://localhost:${port}`));
