import React, { useEffect, useRef } from 'react';
import * as d3 from 'd3';

const colorMap = {
  '*': '#9B59B6', 'Benefit': '#27AE60', 'Benefits': '#E67E22',
  'Candidate': '#5DADE2', 'Certificate': '#566573', 'Certificates': '#7D6608',
  'Company': '#F5B7B1', 'Degree': '#AF7AC5', 'Degrees': '#B9770E',
  'Education': '#EC7063', 'Educations': '#82E0AA', 'Experience': '#F5B7B1',
  'Experiences': '#27AE60', 'JD': '#AF7AC5', 'JobTitle': '#F4D03F',
  'Language': '#F4D03F', 'Languages': '#AF7AC5', 'Location': '#F5B7B1',
  'Locations': '#F4D03F', 'Project': '#48C9B0', 'Projects': '#F39C12',
  'Skill': '#82E0AA', 'Skills': '#E74C3C', 'Task': '#82E0AA', 'Tasks': '#F39C12'
};

export default function Graph() {
  const svgRef = useRef();

  useEffect(() => {
    fetch('http://127.0.0.1:8000/api/graph')
      .then(res => res.json())
      .then(data => {
        const width = 900;
        const height = 700;
        const svg = d3.select(svgRef.current)
          .attr('width', width)
          .attr('height', height)
          .style('border', '1px solid #ccc')
          .style('background', '#1e1e1e');

        svg.selectAll('*').remove();
        const g = svg.append('g');

        svg.call(d3.zoom().scaleExtent([0.1, 5]).on("zoom", (event) => {
          g.attr("transform", event.transform);
        }));

        const tooltip = d3.select('body').append('div')
          .style('position', 'absolute')
          .style('padding', '6px 10px')
          .style('background', 'rgba(0,0,0,0.7)')
          .style('color', '#fff')
          .style('border-radius', '4px')
          .style('pointer-events', 'none')
          .style('opacity', 0);

        const shortLabel = (label) => label.length > 8 ? label.slice(0, 8) + '…' : label;

        // Simulation
        const simulation = d3.forceSimulation(data.nodes)
          .force('link', d3.forceLink(data.links).id(d => d.id).distance(120).strength(1))
          .force('charge', d3.forceManyBody().strength(-400))
          .force('center', d3.forceCenter(width / 2, height / 2))
          .force('collision', d3.forceCollide().radius(20));

        svg.append('defs').append('marker')
          .attr('id', 'arrow')
          .attr('viewBox', '0 -5 10 10')
          .attr('refX', 20)
          .attr('refY', 0)
          .attr('markerWidth', 6)
          .attr('markerHeight', 6)
          .attr('orient', 'auto')
          .append('path')
          .attr('d', 'M0,-5L10,0L0,5')
          .attr('fill', '#999');

        // Map đếm số link giữa 2 node
        const linkCountMap = {};
        data.links.forEach((l, i) => {
          const key = [l.source.id, l.target.id].sort().join('-');
          if (!linkCountMap[key]) linkCountMap[key] = [];
          linkCountMap[key].push(i);
        });

        // Links
        const link = g.append('g')
          .attr('stroke', '#999')
          .attr('stroke-opacity', 0.6)
          .selectAll('line')
          .data(data.links)
          .join('line')
          .attr('stroke-width', 1.5)
          .attr('marker-end', 'url(#arrow)');

        // Nodes
        const node = g.append('g')
          .attr('stroke', '#fff')
          .attr('stroke-width', 1.5)
          .selectAll('circle')
          .data(data.nodes)
          .join('circle')
          .attr('r', 15)
          .attr('fill', d => colorMap[d.label] || '#ccc')
          .call(drag(simulation))
          .on('mouseover', (event, d) => {
            tooltip.transition().duration(200).style('opacity', 1);
            tooltip.html(`<strong>${d.label}</strong>`)
              .style('left', event.pageX + 10 + 'px')
              .style('top', event.pageY + 10 + 'px');
          })
          .on('mousemove', (event) => {
            tooltip.style('left', event.pageX + 10 + 'px').style('top', event.pageY + 10 + 'px');
          })
          .on('mouseout', () => tooltip.transition().duration(200).style('opacity', 0))
          .on('click', (event, d) => alert(`Node details:\nID: ${d.id}\nLabel: ${d.label}`));

        // Node labels
        const label = g.append('g')
          .selectAll('text')
          .data(data.nodes)
          .join('text')
          .text(d => shortLabel(d.label))
          .attr('fill', '#fff')
          .attr('font-size', 12)
          .attr('dx', 18)
          .attr('dy', 4);

        // Link labels
        const linkLabel = g.append('g')
          .selectAll('text')
          .data(data.links)
          .join('text')
          .text(d => d.type)
          .attr('fill', '#aaa')
          .attr('font-size', 10)
          .attr('text-anchor', 'middle')
          .style('pointer-events', 'none');

        // Tick update
        simulation.on('tick', () => {
          link.attr('x1', d => {
            const key = [d.source.id, d.target.id].sort().join('-');
            const index = linkCountMap[key].indexOf(data.links.indexOf(d));
            const total = linkCountMap[key].length;
            const offset = (index - (total - 1) / 2) * 6; // khoảng cách giữa các link
            const dx = d.target.x - d.source.x;
            const dy = d.target.y - d.source.y;
            const len = Math.sqrt(dx*dx + dy*dy);
            return d.source.x - offset * dy / len;
          })
          .attr('y1', d => {
            const key = [d.source.id, d.target.id].sort().join('-');
            const index = linkCountMap[key].indexOf(data.links.indexOf(d));
            const total = linkCountMap[key].length;
            const offset = (index - (total - 1) / 2) * 6;
            const dx = d.target.x - d.source.x;
            const dy = d.target.y - d.source.y;
            const len = Math.sqrt(dx*dx + dy*dy);
            return d.source.y + offset * dx / len;
          })
          .attr('x2', d => {
            const key = [d.source.id, d.target.id].sort().join('-');
            const index = linkCountMap[key].indexOf(data.links.indexOf(d));
            const total = linkCountMap[key].length;
            const offset = (index - (total - 1) / 2) * 6;
            const dx = d.target.x - d.source.x;
            const dy = d.target.y - d.source.y;
            const len = Math.sqrt(dx*dx + dy*dy);
            return d.target.x - offset * dy / len;
          })
          .attr('y2', d => {
            const key = [d.source.id, d.target.id].sort().join('-');
            const index = linkCountMap[key].indexOf(data.links.indexOf(d));
            const total = linkCountMap[key].length;
            const offset = (index - (total - 1) / 2) * 6;
            const dx = d.target.x - d.source.x;
            const dy = d.target.y - d.source.y;
            const len = Math.sqrt(dx*dx + dy*dy);
            return d.target.y + offset * dx / len;
          });

          node.attr('cx', d => d.x).attr('cy', d => d.y);
          label.attr('x', d => d.x).attr('y', d => d.y);
          linkLabel.attr('x', d => (d.source.x + d.target.x)/2)
                   .attr('y', d => (d.source.y + d.target.y)/2);
        });

        function drag(simulation) {
          function dragstarted(event, d) {
            if (!event.active) simulation.alphaTarget(0.3).restart();
            d.fx = d.x;
            d.fy = d.y;
          }
          function dragged(event, d) {
            d.fx = event.x;
            d.fy = event.y;
          }
          function dragended(event, d) {
            if (!event.active) simulation.alphaTarget(0);
            d.fx = null;
            d.fy = null;
          }
          return d3.drag()
            .on('start', dragstarted)
            .on('drag', dragged)
            .on('end', dragended);
        }
      });
  }, []);

  return <svg ref={svgRef}></svg>;
}
