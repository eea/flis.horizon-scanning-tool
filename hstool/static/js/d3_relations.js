var width = $("#svg-relations").width();
var height = 1500;

var svg = d3.select("#svg-relations").append("svg")
    .attr("width", width)
    .attr("height", height);

d3.json("relations", function(error, graph) {

    var ge_width, ge_height;
    var nr_nodes = graph.nodes.length;
    var link_distance;

    if(nr_nodes <=3){
        ge_width = width/6; ge_height = height/7;
        link_distance = ge_width + 40;
    }
    else if(nr_nodes <= 5) {
        ge_width = width/8; ge_height = height/8;
        link_distance = ge_width + 20;
    }
    else if (nr_nodes <=7) {
        ge_width = width /10; ge_height = height /8;
        link_distance = ge_width;
    }
    else if (nr_nodes <=9){
        ge_width = width/10; ge_height = height/8;
        link_distance = ge_width - 20;
    }
    else {
        ge_width = width/14; ge_height = height/10;
        link_distance = ge_width - 40;
    }

    var ellipse_rx = ge_width/5, ellipse_ry=ellipse_rx/2;
    var circle_r = 1/2*ellipse_ry;

    var force = d3.layout.force()
    .charge(-20000)
    .linkDistance(link_distance)
    .size([width, 3/4*height]);

    force
        .nodes(graph.nodes)
        .links(graph.links)
        .start();

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