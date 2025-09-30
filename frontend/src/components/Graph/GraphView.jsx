import React, { useEffect, useState, useRef } from "react";
import ForceGraph2D from "react-force-graph-2d";
import * as d3 from "d3-force";

const GraphView = () => {
  const fgRef = useRef();
  const containerRef = useRef();
  const [data, setData] = useState({ nodes: [], links: [] });
  const [dimensions, setDimensions] = useState({ width: 300, height: 300 });

  // Bảng màu
  const palette = ["#BA29E0", "#2BB5F3", "#6AD7D6", "#E94079", "#DEF169"];

  // Làm nhạt màu
  const lightenColor = (hex, factor = 0.5) => {
    const r = parseInt(hex.substr(1, 2), 16);
    const g = parseInt(hex.substr(3, 2), 16);
    const b = parseInt(hex.substr(5, 2), 16);
    const newR = Math.min(255, Math.floor(r + (255 - r) * factor));
    const newG = Math.min(255, Math.floor(g + (255 - g) * factor));
    const newB = Math.min(255, Math.floor(b + (255 - b) * factor));
    return `rgb(${newR}, ${newG}, ${newB})`;
  };

  // Map label → màu
  const labelColorMap = {};
  let colorIndex = 0;
  const getColor = (node) => {
    const label = node.labels?.[0];
    if (node.properties?.name) {
      if (!labelColorMap[label]) {
        labelColorMap[label] = palette[colorIndex % palette.length];
        colorIndex++;
      }
      return labelColorMap[label];
    }
    if (labelColorMap[label]) {
      return lightenColor(labelColorMap[label], 0.6);
    }
    return "rgba(200,200,200,0.6)";
  };

  // Wrap text
  const wrapText = (ctx, text, x, y, maxWidth, lineHeight) => {
    const words = text.split(" ");
    let line = "";
    let lines = [];
    for (let n = 0; n < words.length; n++) {
      let testLine = line + words[n] + " ";
      let metrics = ctx.measureText(testLine);
      let testWidth = metrics.width;
      if (testWidth > maxWidth && n > 0) {
        lines.push(line.trim());
        line = words[n] + " ";
      } else {
        line = testLine;
      }
    }
    lines.push(line.trim());
    lines.forEach((l, i) => {
      ctx.fillText(l, x, y + i * lineHeight);
    });
  };

  useEffect(() => {
    fetch("http://localhost:4000/graph")
      .then((res) => res.json())
      .then((graph) => {
        setData(graph);
        setTimeout(() => {
          fgRef.current.zoomToFit(500, 100);
        }, 500);
      });
  }, []);

  // Lắng nghe thay đổi kích thước container
  useEffect(() => {
    const resizeObserver = new ResizeObserver((entries) => {
      if (entries[0]) {
        const { width, height } = entries[0].contentRect;
        setDimensions({ width, height });
      }
    });
    if (containerRef.current) {
      resizeObserver.observe(containerRef.current);
    }
    return () => resizeObserver.disconnect();
  }, []);

  return (
    <div
      ref={containerRef}
      className="bg-[#19335A] w-full h-full"
      style={{
        background:
          "radial-gradient(circle,rgba(233, 234, 245, 1) 2%, rgba(25, 51, 90, 1) 88%)",
      }}
    >
      <ForceGraph2D
        ref={fgRef}
        width={dimensions.width}
        height={dimensions.height}
        graphData={data}
        nodeLabel={(node) =>
          `${node.labels?.[0]}: ${node.properties?.name || ""}`
        }
        linkLabel={(link) => link.type}
        nodeCanvasObject={(node, ctx, globalScale) => {
          const label = node.properties?.name || node.id;
          const fontSize = 11 / globalScale;
          const radius = node.properties?.name ? 8 : 20;

          ctx.beginPath();
          ctx.arc(node.x, node.y, radius, 0, 2 * Math.PI, false);
          ctx.fillStyle = getColor(node);
          ctx.fill();
          ctx.strokeStyle = "#eee";
          ctx.lineWidth = 0.4;
          ctx.stroke();

          ctx.font = `${fontSize}px Sans-Serif`;
          ctx.fillStyle = "#000";
          ctx.textAlign = "center";
          ctx.textBaseline = "middle";

          wrapText(
            ctx,
            label,
            node.x,
            node.y - fontSize / 2,
            radius * 2.5,
            fontSize + 2
          );
        }}
        linkColor={() => "#eeeeff"}
        linkDirectionalArrowLength={4}
        linkDirectionalArrowRelPos={1}
        backgroundColor="#121212"
        d3Force={(fg) => {
          fg.d3Force("charge").strength(-800);
          fg.d3Force("link").distance(800);
          fg.d3Force(
            "collision",
            d3
              .forceCollide()
              .radius((node) => (node.properties?.name ? 30 : 15))
          );
        }}
      />
    </div>
  );
};

export default GraphView;
