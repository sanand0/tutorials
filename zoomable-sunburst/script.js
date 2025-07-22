import { bootstrapAlert } from "https://cdn.jsdelivr.net/npm/bootstrap-alert@1";

const fullData = await d3.csv("companies.csv");

// Populate the root companies in the selector
const roots = [...new Set(fullData.map((d) => d.root))];
d3.select("#root-selector")
  .selectAll("option")
  .data(roots)
  .join("option")
  .text((d) => d);

function drawSunburst() {
  // Filter by current company
  const company = document.querySelector("#root-selector").value;
  const data = fullData.filter((d) => d.root == company);
  console.log(data);

  // Set up the SVG container layout
  const width = 1000;
  const height = width;
  const radius = width / 6;
  const svg = d3.select("#sunburst");
  svg.attr("viewBox", [-width / 2, -height / 2, width, width]);
  svg.selectAll("*").remove();

  // Compute the hierarchy
  const root = d3
    .stratify() // turn flat table → tree
    .id((d) => d.company) // node key
    // lookup key of its parent
    .parentId((d) => d.parent)(data) // build the hierarchy
    .sum(() => 1) // every company counts as 1
    .sort((a, b) => b.value - a.value); // biggest slices outside‑in

  // Create the color scale.
  const color = d3.scaleOrdinal(d3.quantize(d3.interpolateRainbow, root.children.length + 1));

  // Create the layout
  d3
    .partition() // polar “sunburst” layout
    // full circle, depth = radius
    .size([2 * Math.PI, root.height + 1])(root);
  root.each((d) => (d.current = d)); // helper for zoom / animation

  // Create the arc generator.
  const arc = d3
    .arc()
    .startAngle((d) => d.x0)
    .endAngle((d) => d.x1)
    .padAngle((d) => Math.min((d.x1 - d.x0) / 2, 0.005))
    .padRadius(radius * 1.5)
    .innerRadius((d) => d.y0 * radius)
    .outerRadius((d) => Math.max(d.y0 * radius, d.y1 * radius - 1));

  // Append the arcs.
  const path = svg
    .append("g")
    .selectAll("path")
    .data(root.descendants().slice(1))
    .join("path")
    .attr("fill", (d) => {
      while (d.depth > 1) d = d.parent;
      return color(d.data.company);
    })
    .attr("fill-opacity", (d) => (arcVisible(d.current) ? (d.children ? 0.6 : 0.4) : 0))
    .attr("pointer-events", (d) => (arcVisible(d.current) ? "auto" : "none"))
    .attr("d", (d) => arc(d.current));

  // Make them clickable if they have children.
  path
    .filter((d) => d.children)
    .style("cursor", "pointer")
    .on("click", clicked);

  // Add central label
  const centerLabel = svg
    .append("text")
    .attr("text-anchor", "middle")
    .attr("dy", "0.35em")
    .attr("font-size", "1.5em")
    .text(root.data.company);

  // Helper functions for tooltip info
  function countChildren(d) {
    return d.children ? d.children.length : 0;
  }

  function countDescendants(d) {
    return d.descendants().length - 1; // -1 to exclude self
  }

  // Update tooltip content
  path
    .append("title")
    .text(
      (d) =>
        `Company: ${d.data.company}\n` +
        `Parent: ${d.parent ? d.parent.data.company : "None"}\n` +
        `Children: ${countChildren(d)}\n` +
        `Descendants: ${countDescendants(d)}`
    );

  const label = svg
    .append("g")
    .attr("pointer-events", "none")
    .attr("text-anchor", "middle")
    .style("user-select", "none")
    .selectAll("text")
    .data(root.descendants().slice(1))
    .join("text")
    .attr("dy", "0.35em")
    .attr("fill-opacity", (d) => +labelVisible(d.current))
    .attr("transform", (d) => labelTransform(d.current))
    .text((d) => d.data.company);

  const parent = svg
    .append("circle")
    .datum(root)
    .attr("r", radius)
    .attr("fill", "none")
    .attr("pointer-events", "all")
    .on("click", clicked);

  // Handle zoom on click.
  function clicked(event, p) {
    parent.datum(p.parent || root);

    // Update center label
    centerLabel.text(p.data.company);

    root.each(
      (d) =>
        (d.target = {
          x0: Math.max(0, Math.min(1, (d.x0 - p.x0) / (p.x1 - p.x0))) * 2 * Math.PI,
          x1: Math.max(0, Math.min(1, (d.x1 - p.x0) / (p.x1 - p.x0))) * 2 * Math.PI,
          y0: Math.max(0, d.y0 - p.depth),
          y1: Math.max(0, d.y1 - p.depth),
        })
    );

    const t = svg.transition().duration(event.altKey ? 7500 : 750);

    // Transition the data on all arcs, even the ones that aren’t visible,
    // so that if this transition is interrupted, entering arcs will start
    // the next transition from the desired position.
    path
      .transition(t)
      .tween("data", (d) => {
        const i = d3.interpolate(d.current, d.target);
        return (t) => (d.current = i(t));
      })
      .filter(function (d) {
        return +this.getAttribute("fill-opacity") || arcVisible(d.target);
      })
      .attr("fill-opacity", (d) => (arcVisible(d.target) ? (d.children ? 0.6 : 0.4) : 0))
      .attr("pointer-events", (d) => (arcVisible(d.target) ? "auto" : "none"))

      .attrTween("d", (d) => () => arc(d.current));

    label
      .filter(function (d) {
        return +this.getAttribute("fill-opacity") || labelVisible(d.target);
      })
      .transition(t)
      .attr("fill-opacity", (d) => +labelVisible(d.target))
      .attrTween("transform", (d) => () => labelTransform(d.current));
  }

  function arcVisible(d) {
    return d.y1 <= 3 && d.y0 >= 1 && d.x1 > d.x0;
  }

  function labelVisible(d) {
    return d.y1 <= 3 && d.y0 >= 1 && (d.y1 - d.y0) * (d.x1 - d.x0) > 0.03;
  }

  function labelTransform(d) {
    const x = (((d.x0 + d.x1) / 2) * 180) / Math.PI;
    const y = ((d.y0 + d.y1) / 2) * radius;
    return `rotate(${x - 90}) translate(${y},0) rotate(${x < 180 ? 0 : 180})`;
  }

  return svg.node();
}

document.querySelector("#root-selector").addEventListener("change", drawSunburst);
drawSunburst();
