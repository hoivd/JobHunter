import React, { useEffect, useRef } from "react";
import * as d3 from "d3";

// --- [PALETTE] ---
const palette = {
  forest: { dark: "#215732", mid: "#4C9141", light: "#A7D08C" },
  marigold: { dark: "#FF8C00", mid: "#FFB347", light: "#FFD580" },
  hibiscus: { dark: "#E32636", mid: "#F75C57", light: "#F6A5A1" },
};

// --- [MAPPING] ---
const colorMap = {
  JD: palette.forest.dark,
  Candidate: palette.hibiscus.dark,
  Company: palette.marigold.dark,
  Project: palette.forest.dark,
  Experience: palette.marigold.dark,
  Education: palette.hibiscus.dark,

  Skills: palette.forest.mid,
  Certificates: palette.marigold.mid,
  Tasks: palette.hibiscus.mid,
  Locations: palette.forest.mid,
  Languages: palette.marigold.mid,
  Degrees: palette.hibiscus.mid,
  Benefits: palette.marigold.mid,

  Skill: palette.forest.light,
  Certificate: palette.marigold.light,
  Task: palette.hibiscus.light,
  Location: palette.forest.light,
  Language: palette.marigold.light,
  Degree: palette.hibiscus.light,
  Benefit: palette.marigold.light,

  "*": "#ccc",
};

const lightColors = [palette.hibiscus.light];
function randomLight() {
  return lightColors[Math.floor(Math.random() * lightColors.length)];
}

function drag(simulation) {
  return d3
    .drag()
    .on("start", (event, d) => {
      if (!event.active) simulation.alphaTarget(0.3).restart();
      d.fx = d.x;
      d.fy = d.y;
    })
    .on("drag", (event, d) => {
      d.fx = event.x;
      d.fy = event.y;
    })
    .on("end", (event, d) => {
      if (!event.active) simulation.alphaTarget(0);
      d.fx = null;
      d.fy = null;
    });
}

export default function Graph() {
  const svgRef = useRef();

  useEffect(() => {
    const width = 1000;
    const height = 800;

    const svg = d3
      .select(svgRef.current)
      .attr("width", width)
      .attr("height", height)
      .style("border", "1px solid #ccc")
      .style("background", "#1e1e1e");

    svg.selectAll("*").remove();

    const g = svg.append("g");

    // --- [ZOOM] ---
    svg.call(
      d3
        .zoom()
        .scaleExtent([0.2, 5])
        .on("zoom", (event) => {
          g.attr("transform", event.transform);
        })
    );

    // --- [TOOLTIP] ---
    const tooltip = d3
      .select("body")
      .append("div")
      .attr("class", "graph-tooltip")
      .style("position", "absolute")
      .style("padding", "8px 12px")
      .style("background", "rgba(0,0,0,0.85)")
      .style("color", "#fff")
      .style("border-radius", "6px")
      .style("font-size", "13px")
      .style("max-width", "280px")
      .style("pointer-events", "none")
      .style("opacity", 0);

    fetch("http://127.0.0.1:8000/api/graph")
      .then((res) => res.json())
      .then((data) => {
        // --- link song song ---
        const linkCounts = {};
        data.links.forEach((l) => {
          const key = [l.source, l.target].sort().join("-");
          linkCounts[key] = (linkCounts[key] || 0) + 1;
          l.linkIndex = linkCounts[key];
        });

        // --- [FORCE SIMULATION] ---
        const simulation = d3
          .forceSimulation(data.nodes)
          .force(
            "link",
            d3
              .forceLink(data.links)
              .id((d) => d.id)
              .distance((d) => {
                if (
                  d.source.properties?.type === "main" &&
                  d.target.properties?.type === "property"
                ) {
                  return 150; // main ↔ property xa hơn
                }
                if (
                  d.target.properties?.type === "main" &&
                  d.source.properties?.type === "property"
                ) {
                  return 150;
                }
                return 80; // mặc định
              })
          )

          .force("charge", d3.forceManyBody().strength(-250))
          .force("center", d3.forceCenter(width / 2, height / 2))
          .force("collision", d3.forceCollide().radius(30));

        // --- [ARROW MARKER nhỏ hơn] ---
        svg
          .append("defs")
          .append("marker")
          .attr("id", "arrowhead")
          .attr("viewBox", "0 -5 10 10")
          .attr("refX", 45)
          .attr("refY", 0)
          .attr("markerWidth", 3)
          .attr("markerHeight", 3)
          .attr("orient", "auto")
          .append("path")
          .attr("d", "M0,-5L10,0L0,5")
          .attr("fill", "#bbb");

        // --- [LINKS] ---
        const link = g
          .append("g")
          .attr("stroke", "#aaa")
          .attr("stroke-opacity", 0.6)
          .selectAll("path")
          .data(data.links)
          .join("path")
          .attr("stroke-width", 2.0)
          .attr("fill", "none")
          .attr("marker-end", "url(#arrowhead)")
          .attr("id", (d, i) => `link-${i}`)
          .style("cursor", "pointer"); // 🔹 hover vào link = pointer

        // --- [NODES] ---
        const node = g
          .append("g")
          .selectAll("circle")
          .data(data.nodes)
          .join("circle")
          .attr("r", (d) => {
            if (d.label === "Skills") return 32;
            if (
              [
                "Skill",
                "Certificate",
                "Task",
                "Location",
                "Language",
                "Degree",
                "Benefit",
              ].includes(d.label)
            )
              return 16;
            return 22;
          })
          .attr("fill", (d) =>
            colorMap[d.label] ? colorMap[d.label] : randomLight()
          )
          .attr("stroke", "#fff")
          .attr("stroke-width", 1.5)
          .call(drag(simulation))
          .on("mouseover", (event, d) => {
            tooltip.transition().duration(200).style("opacity", 0.9);
            tooltip
              .html(
                `<div>${d.label}</div>
                 ${
                   d.properties
                     ? `<div><strong>Properties:</strong><br/>${Object.entries(
                         d.properties
                       )
                         .map(([k, v]) => `${k}: ${v}`)
                         .join("<br/>")}</div>`
                     : ""
                 }`
              )
              .style("left", event.pageX + 12 + "px")
              .style("top", event.pageY + 12 + "px");
          })
          .on("mousemove", (event) =>
            tooltip
              .style("left", event.pageX + 12 + "px")
              .style("top", event.pageY + 12 + "px")
          )
          .on("mouseout", () =>
            tooltip.transition().duration(200).style("opacity", 0)
          );

        // --- [NODE LABELS] ---
        const shortLabel = (label) =>
          label.length > 10 ? label.slice(0, 10) + "…" : label;

        const nodeLabel = g
          .append("g")
          .selectAll("text")
          .data(data.nodes)
          .join("text")
          .text((d) => shortLabel(d.label))
          .attr("fill", "#000")
          .attr("font-size", 9)
          .attr("text-anchor", "middle")
          .attr("dy", 3);

        // --- [RELATIONSHIP LABELS] (ẩn mặc định) ---
        const linkLabel = g
          .append("g")
          .selectAll("text")
          .data(data.links)
          .join("text")
          .attr("font-size", 6)
          .attr("fill", "#FFD700")
          .style("opacity", 0) // 🔹 ẩn mặc định
          .append("textPath")
          .attr("xlink:href", (d, i) => `#link-${i}`)
          .attr("startOffset", "50%")
          .style("text-anchor", "middle")
          .text((d) => d.type)
          .attr("font-size", 12);

        // --- hover vào link thì hiện label ---
        link
          .on("mouseover", function (event, d) {
            d3.select(this).attr("stroke", "#FFD700");
            g.selectAll("text")
              .filter((l) => l === d) // lọc đúng label link đó
              .style("opacity", 1);
          })
          .on("mouseout", function (event, d) {
            d3.select(this).attr("stroke", "#aaa");
            g.selectAll("text")
              .filter((l) => l === d)
              .style("opacity", 0);
          });

        // --- [TICK UPDATE] ---
        simulation.on("tick", () => {
          link.attr("d", (d) => {
            const dx = d.target.x - d.source.x;
            const dy = d.target.y - d.source.y;
            const dr = Math.sqrt(dx * dx + dy * dy);

            const angle = Math.atan2(dy, dx);
            const offset = (d.linkIndex - 1) * 30;

            const mx =
              (d.source.x + d.target.x) / 2 +
              offset * Math.cos(angle + Math.PI / 2);
            const my =
              (d.source.y + d.target.y) / 2 +
              offset * Math.sin(angle + Math.PI / 2);

            return `M${d.source.x},${d.source.y} Q${mx},${my} ${d.target.x},${d.target.y}`;
          });

          node.attr("cx", (d) => d.x).attr("cy", (d) => d.y);
          nodeLabel.attr("x", (d) => d.x).attr("y", (d) => d.y);
        });

        return () => {
          simulation.stop();
          tooltip.remove();
        };
      });
  }, []);

  return <svg ref={svgRef}></svg>;
}
