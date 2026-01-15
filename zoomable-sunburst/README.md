# How to create a zoomable sunburst with company hierarchy with LLMs

## Generate realistic fake data

[ChatGPT](https://chatgpt.com/share/687e1fac-bf20-800c-a19f-05a3d1b812ee)

It's important to ask for data that will showcase the results we want.
Here is the prompt sequence I used.

> Write a program to generate REALISTIC fake data for company hierarchies.
> The data should have 3 columns:
>
> 1. company: a company name
> 2. parent: parent company name that owns company
> 3. root: an ultimate parent company name
>
> Generate 15 different unique roots.
> For each root, generate a set of children, some of them having more children, some of which having more children, and so on.
> I will be visualizing this as a sunburst, so keep the maximum depth to 5 (including root and leaf), and make sure that ~20% (customizable) at each level does not have children.
>
> Generate realistic company names using a faker library.
> Use either Python or NodeJS, whichever has a better faker library for company names.

I got an error.

> faker.exceptions.UniquenessException: Got duplicated values after 1,000 iterations.

I also wanted reproducibility.

> Add a random seed

With that, we now have [fake.py](fake.py) and `uv run fake.py` generates [companies.csv](companies.csv)

## Generate visualization with Cursor

I tried this with [Cursor](https://cursor.com/) - free account:

> Update index.html and script.js to create an interactive single page web application.
> This shows a beautiful responsive animated zoomable D3 v7 sunburst fetching data in companies.csv.
> Allow the user to choose a Root company via unique values of the `root` column.
> Filter all rows with that root.
> Start with the root at the center and generate the zoomable sunburst.
> All leaf companies have the same angle.
> All parents have an angle proportional to the sum of their descendents angle.
> Pick distinct, elegant colors with hues based on the top level children and saturation / lightness based on the levels.
> Show labels with the company names.
> Rotate the labels so that they align with radii and are never turned upside down, hence always readable.
> Use borders with the same color as the background - use Bootstrap var(--bs-body-bg) for this.
> The title says, "Company hierarchy".
> Add a legend at the bottom explaining how to zoom in and out.

... but that created an output that didn't work. I didn't explore why.

## Generate visualization with Claude Code

I switched to [Claude Code](https://www.anthropic.com/claude-code) and added these instructions:

> Style:
>
> - Write SHORT, CONCISE, READABLE code
> - Deduplicate maximally. Use iteration, higher-order functions, vectorization
> - Validate early. Use the if-return pattern. Avoid unnecessary else statements
> - Avoid try blocks unless the operation is error-prone
> - Use functions, not classes
> - Use ESM: `<script type="module">`
> - No TypeScript. Only JavaScript
> - Use MODERN JavaScript. Minimize libraries
> - Use hyphenated HTML class/ID names (id="user-id" not id="userId")
> - For single line if / for statements, avoid { blocks }
> - Show a loading indicator while waiting for fetch()
> - Use Bootstrap classes for CSS. Avoid custom CSS
> - Use D3 for data visualization
>
> Show errors to the user using bootstrapAlert:
>
> ```
> import { bootstrapAlert } from "https://cdn.jsdelivr.net/npm/bootstrap-alert@1";
> // Simple toast
> bootstrapAlert("Simple message");
> // Custom toast: with title and color
> bootstrapAlert({ title: "Success", body: "Custom toast message", color: "success" });
> ```

This generated an output at a cost of 22 cents but was not zoomable. So I switched.

## Generate visualization with Cursor

> Update index.html and script.js to create an interactive single page web application.
> This shows a beautiful responsive animated zoomable D3 v7 sunburst fetching data in companies.csv.
> Allow the user to choose a Root company via unique values of the `root` column.
> Filter all rows with that root.
> Start with the root at the center and generate the zoomable sunburst.
> All leaf companies have the same angle.
> All parents have an angle proportional to the sum of their descendents angle.
> Pick distinct, elegant colors with hues based on the top level children and saturation / lightness based on the levels.
> Hovering over each arc shows the company name, number of children, and number of descendents as a D3 tooltip.
> Use borders with the same color as the background - use Bootstrap var(--bs-body-bg) for this.
> The title says, "Company hierarchy".
> Add a legend at the bottom explaining how to zoom in and out.
>
> Show errors to the user using bootstrapAlert:
>
> ```
> import { bootstrapAlert } from "https://cdn.jsdelivr.net/npm/bootstrap-alert@1";
> // Simple toast
> bootstrapAlert("Simple message");
> // Custom toast: with title and color
> bootstrapAlert({ title: "Success", body: "Custom toast message", color: "success" });
> ```
>
> Use the sample code here as a reference for zoomable sunbursts. Don't show company names as labels -- only show them as D3 tooltips.
>
> ```js
> chart = {
>   // Specify the chart’s dimensions.
>   const width = 928;
>   const height = width;
>   const radius = width / 6;
>
>   // Create the color scale.
>   const color = d3.scaleOrdinal(d3.quantize(d3.interpolateRainbow, data.children.length + 1));
>
>   // Compute the layout.
>   const hierarchy = d3.hierarchy(data)
>       .sum(d => d.value)
>       .sort((a, b) => b.value - a.value);
>   const root = d3.partition()
>       .size([2 * Math.PI, hierarchy.height + 1])
>     (hierarchy);
>   root.each(d => d.current = d);
>
>   // Create the arc generator.
>   const arc = d3.arc()
>       .startAngle(d => d.x0)
>       .endAngle(d => d.x1)
>       .padAngle(d => Math.min((d.x1 - d.x0) / 2, 0.005))
>       .padRadius(radius * 1.5)
>       .innerRadius(d => d.y0 * radius)
>       .outerRadius(d => Math.max(d.y0 * radius, d.y1 * radius - 1))
>
>   // Create the SVG container.
>   const svg = d3.create("svg")
>       .attr("viewBox", [-width / 2, -height / 2, width, width])
>       .style("font", "10px sans-serif");
>
>   // Append the arcs.
>   const path = svg.append("g")
>     .selectAll("path")
>     .data(root.descendants().slice(1))
>     .join("path")
>       .attr("fill", d => { while (d.depth > 1) d = d.parent; return color(d.data.name); })
>       .attr("fill-opacity", d => arcVisible(d.current) ? (d.children ? 0.6 : 0.4) : 0)
>       .attr("pointer-events", d => arcVisible(d.current) ? "auto" : "none")
>       .attr("d", d => arc(d.current));
>
>   // Make them clickable if they have children.
>   path.filter(d => d.children)
>       .style("cursor", "pointer")
>       .on("click", clicked);
>
>   const format = d3.format(",d");
>   path.append("title")
>       .text(d => `${d.ancestors().map(d => d.data.name).reverse().join("/")}\n${format(d.value)}`);
>
>   const label = svg.append("g")
>       .attr("pointer-events", "none")
>       .attr("text-anchor", "middle")
>       .style("user-select", "none")
>     .selectAll("text")
>     .data(root.descendants().slice(1))
>     .join("text")
>       .attr("dy", "0.35em")
>       .attr("fill-opacity", d => +labelVisible(d.current))
>       .attr("transform", d => labelTransform(d.current))
>       .text(d => d.data.name);
>
>   const parent = svg.append("circle")
>       .datum(root)
>       .attr("r", radius)
>       .attr("fill", "none")
>       .attr("pointer-events", "all")
>       .on("click", clicked);
>
>   // Handle zoom on click.
>   function clicked(event, p) {
>     parent.datum(p.parent || root);
>
>     root.each(d => d.target = {
>       x0: Math.max(0, Math.min(1, (d.x0 - p.x0) / (p.x1 - p.x0))) * 2 * Math.PI,
>       x1: Math.max(0, Math.min(1, (d.x1 - p.x0) / (p.x1 - p.x0))) * 2 * Math.PI,
>       y0: Math.max(0, d.y0 - p.depth),
>       y1: Math.max(0, d.y1 - p.depth)
>     });
>
>     const t = svg.transition().duration(event.altKey ? 7500 : 750);
>
>     // Transition the data on all arcs, even the ones that aren’t visible,
>     // so that if this transition is interrupted, entering arcs will start
>     // the next transition from the desired position.
>     path.transition(t)
>         .tween("data", d => {
>           const i = d3.interpolate(d.current, d.target);
>           return t => d.current = i(t);
>         })
>       .filter(function(d) {
>         return +this.getAttribute("fill-opacity") || arcVisible(d.target);
>       })
>         .attr("fill-opacity", d => arcVisible(d.target) ? (d.children ? 0.6 : 0.4) : 0)
>         .attr("pointer-events", d => arcVisible(d.target) ? "auto" : "none")
>
>         .attrTween("d", d => () => arc(d.current));
>
>     label.filter(function(d) {
>         return +this.getAttribute("fill-opacity") || labelVisible(d.target);
>       }).transition(t)
>         .attr("fill-opacity", d => +labelVisible(d.target))
>         .attrTween("transform", d => () => labelTransform(d.current));
>   }
>
>   function arcVisible(d) {
>     return d.y1 <= 3 && d.y0 >= 1 && d.x1 > d.x0;
>   }
>
>   function labelVisible(d) {
>     return d.y1 <= 3 && d.y0 >= 1 && (d.y1 - d.y0) * (d.x1 - d.x0) > 0.03;
>   }
>
>   function labelTransform(d) {
>     const x = (d.x0 + d.x1) / 2 * 180 / Math.PI;
>     const y = (d.y0 + d.y1) / 2 * radius;
>     return `rotate(${x - 90}) translate(${y},0) rotate(${x < 180 ? 0 : 180})`;
>   }
>
>   return svg.node();
> }
> ```

This didn't work either.

## Write it manually

Finally, I just decided to code manually, mostly copying from <https://observablehq.com/@d3/zoomable-sunburst>.

This took about 40 min -- roughly 2X the time I spent vibe-coding.

## Takeaway

Sometimes, vibe-coding works. Sometimes, it doesn't. Don't rely on it for important deliverables.
