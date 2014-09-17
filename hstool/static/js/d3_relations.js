var width = 1000, height = 1000;

var force = d3.layout.force()
    .charge(-10000)
    .linkDistance(150)
    .size([width, 3/4*height]);

var svg = d3.select("#svg-relations").append("svg")
    .attr("width", width)
    .attr("height", height);

d3.json("relations", function(error, graph) {
    force
        .nodes(graph.nodes)
        .links(graph.links)
        .start();

    var ge_width = 100, ge_height = 140;
    var ellipse_rx = 30, ellipse_ry=15;
    var circle_r = 1/2*ellipse_ry;

    //Relation
    var link = svg.selectAll(".link")
        .data(graph.links).enter()
        .append("line")
        .attr("class", "link");

    var ellipse = svg.selectAll()
        .data(graph.links).enter()
        .append("ellipse")
        .attr("class", "ellipse")
        .attr("rx", ellipse_rx)
        .attr("ry", ellipse_ry);

    var link_circle = svg.selectAll()
        .data(graph.links).enter()
        .append("circle")
        .attr("class", "circle")
        .attr("r", circle_r);

    var link_line_1 = svg.selectAll()
        .data(graph.links).enter()
        .append("line")
        .attr("class", "line");

    var link_line_2 = svg.selectAll()
        .data(graph.links).enter()
        .append("line")
        .attr("class", "line");

    // Generic Element
    var node = svg.selectAll(".node")
        .data(graph.nodes).enter()
        .append("rect")
        .attr("class", "node")
        .attr("width", ge_width)
        .attr("height", ge_height);

    var box1 = svg.selectAll()
        .data(graph.nodes).enter()
        .append("rect")
        .attr("class", "box1")
        .attr("width", ge_width)
        .attr("height", ge_height/6);

    var title = svg.selectAll()
        .data(graph.nodes).enter()
        .append("text")
        .attr("class", "text")
        .text(function(d) { return d.name });

    var box2 = svg.selectAll()
        .data(graph.nodes).enter()
        .append("rect")
        .attr("class", "box2")
        .attr("width", ge_width)
        .attr("height", ge_height/6);

    var trend = svg.selectAll()
        .data(graph.nodes).enter()
        .append("text")
        .attr("class", "text")
        .text(function(d) { return d.trend });

    var node_circle = svg.selectAll()
        .data(graph.nodes).enter()
        .append("circle")
        .attr("class", "circle")
        .attr("r", circle_r);

    var node_line_1 = svg.selectAll()
        .data(graph.nodes).enter()
        .append("line")
        .attr("class", "line");

    var node_line_2 = svg.selectAll()
        .data(graph.nodes).enter()
        .append("line")
        .attr("class", "line");

    force.on("tick", function() {
        // Links
        link.attr("x1", function(d) { return d.source.x + ge_width/2; })
            .attr("y1", function(d) { return d.source.y + ge_height/2; })
            .attr("x2", function(d) { return d.target.x + ge_width/2; })
            .attr("y2", function(d) { return d.target.y + ge_height/2;  });

        ellipse
            .attr("cx", function(d) { return (d.source.x + ge_width/2 + d.target.x + ge_width/2)/2; })
            .attr("cy", function(d) { return (d.source.y + ge_height/2 + d.target.y + ge_height/2)/2; });

        link_circle
            .attr("cx", function(d) { return (d.source.x + ge_width/2 + d.target.x + ge_width/2)/2; })
            .attr("cy", function(d) { return (d.source.y + ge_height/2 + d.target.y + ge_height/2)/2 + ellipse_ry - circle_r; });

        link_line_1
            .attr("x1", function(d) { return (d.source.x + ge_width/2 + d.target.x + ge_width/2)/2 - circle_r + 3; })
            .attr("y1", function(d) { return (d.source.y + ge_height/2 + d.target.y + ge_height/2)/2 + ellipse_ry - circle_r; })
            .attr("x2", function(d) { return (d.source.x + ge_width/2 + d.target.x + ge_width/2)/2 + circle_r - 3; })
            .attr("y2", function(d) { return (d.source.y + ge_height/2 + d.target.y + ge_height/2)/2 + ellipse_ry - circle_r; });

        link_line_2
            .attr("x1", function(d) { return (d.source.x + ge_width/2 + d.target.x + ge_width/2)/2; })
            .attr("y1", function(d) { return (d.source.y + ge_height/2 + d.target.y + ge_height/2)/2 + ellipse_ry - circle_r - circle_r + 3; })
            .attr("x2", function(d) { return (d.source.x + ge_width/2 + d.target.x + ge_width/2)/2; })
            .attr("y2", function(d) { return (d.source.y + ge_height/2 + d.target.y + ge_height/2)/2 + ellipse_ry - circle_r + circle_r - 3; });

        // Generic Elements
        node.attr("x", function(d) { return d.x; })
            .attr("y", function(d) { return d.y; });

        box1.attr("x", function(d) { return d.x; })
            .attr("y", function(d) { return d.y; });

        title
            .attr("x", function(d) { return d.x + ge_width/2; })
            .attr("y", function(d) { return d.y + ge_height/12 + 5 });

        box2.attr("x", function(d) { return d.x; })
            .attr("y", function(d) { return d.y + ge_height/6; });

        trend
            .attr("x", function(d) { return d.x + ge_width/2; })
            .attr("y", function(d) { return d.y + ge_height/12 + + ge_height/6 + 5 });

        node_circle
            .attr("cx", function(d) { return (d.x + ge_width - circle_r - 10); })
            .attr("cy", function(d) { return (d.y + ge_height - circle_r - 10); });

        node_line_1
            .attr("x1", function(d) { return (d.x + ge_width - circle_r - 10 - circle_r + 3)})
            .attr("y1", function(d) { return (d.y + ge_height - circle_r - 10)})
            .attr("x2", function(d) { return (d.x + ge_width - circle_r - 10 + circle_r - 3)})
            .attr("y2", function(d) { return (d.y + ge_height - circle_r - 10)});

        node_line_2
            .attr("x1", function(d) { return (d.x + ge_width - circle_r - 10)})
            .attr("y1", function(d) { return (d.y + ge_height - circle_r - 10 - circle_r + 3)})
            .attr("x2", function(d) { return (d.x + ge_width - circle_r - 10)})
            .attr("y2", function(d) { return (d.y + ge_height - circle_r - 10 + circle_r - 3)});
    });
});