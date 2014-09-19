var width = $("#svg-relations").width();
var height = width;

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
        .size([width, 3/4*height])
        .nodes(graph.nodes)
        .links(graph.links)
        .start();

    for(var i=0;i<200;i++){
        force.tick();
    }
    force.stop();

    //Draw relation
    var links = svg.selectAll()
        .data(graph.links).enter();

    links
        .append("line")
        .attr("class", "link")
        .attr("x1", function(d) { return d.source.x + ge_width/2; })
        .attr("y1", function(d) { return d.source.y + ge_height/2; })
        .attr("x2", function(d) { return d.target.x + ge_width/2; })
        .attr("y2", function(d) { return d.target.y + ge_height/2;  });

    links
        .append("ellipse")
        .attr("class", "ellipse")
        .attr("rx", ellipse_rx)
        .attr("ry", ellipse_ry)
        .attr("cx", function(d) { return (d.source.x + ge_width/2 + d.target.x + ge_width/2)/2; })
        .attr("cy", function(d) { return (d.source.y + ge_height/2 + d.target.y + ge_height/2)/2; });

    links
        .append("a")
        .attr("class", "launch-node-modal")
        .attr("data-toggle", "modal")
        .attr("data-target", "#myModal")
        .on("click", function(d) {
            var url = d.url;
            $.ajax({
                type: "GET",
                url: url,
                success: function (data) {
                    $('.modal-body').html(data);
                },
                error: function () {
                    alert('Error launching the modal')
                }
            })
        })
        .append("circle")
        .attr("class", "circle")
        .attr("r", circle_r)
        .attr("cx", function(d) { return (d.source.x + ge_width/2 + d.target.x + ge_width/2)/2; })
        .attr("cy", function(d) { return (d.source.y + ge_height/2 + d.target.y + ge_height/2)/2 + ellipse_ry - circle_r; });

    links
        .append("line")
        .attr("class", "line")
        .attr("x1", function(d) { return (d.source.x + ge_width/2 + d.target.x + ge_width/2)/2 - circle_r + 3; })
        .attr("y1", function(d) { return (d.source.y + ge_height/2 + d.target.y + ge_height/2)/2 + ellipse_ry - circle_r; })
        .attr("x2", function(d) { return (d.source.x + ge_width/2 + d.target.x + ge_width/2)/2 + circle_r - 3; })
        .attr("y2", function(d) { return (d.source.y + ge_height/2 + d.target.y + ge_height/2)/2 + ellipse_ry - circle_r; });

    links
        .append("line")
        .attr("class", "line")
        .attr("x1", function(d) { return (d.source.x + ge_width/2 + d.target.x + ge_width/2)/2; })
        .attr("y1", function(d) { return (d.source.y + ge_height/2 + d.target.y + ge_height/2)/2 + ellipse_ry - circle_r - circle_r + 3; })
        .attr("x2", function(d) { return (d.source.x + ge_width/2 + d.target.x + ge_width/2)/2; })
        .attr("y2", function(d) { return (d.source.y + ge_height/2 + d.target.y + ge_height/2)/2 + ellipse_ry - circle_r + circle_r - 3; });

    //Draw Generic Element
    var nodes = svg.selectAll(".node")
        .data(graph.nodes).enter();

    nodes
        .append("rect")
        .attr("class", "node")
        .attr("width", ge_width)
        .attr("height", ge_height)
        .attr("x", function(d) { return d.x; })
        .attr("y", function(d) { return d.y; });

    nodes
        .append("text")
        .attr("class", "text")
        .text(function(d) { return d.title })
        .attr("x", function(d) { return d.x + ge_width/2; })
        .attr("y", function(d) { return d.y + ge_height/12 + 5 });

    nodes
        .append("rect")
        .attr("class", function(d) { switch (d.subtitle_color) {
                case 0: return "box-salmon";
                case 1: return "box-purple";
                case 2: return "box-pink";

        }})
        .attr("width", ge_width)
        .attr("height", ge_height/6)
        .attr("x", function(d) { return d.x; })
        .attr("y", function(d) { return d.y + ge_height/6; });

    nodes
        .append("text")
        .attr("class", "text")
        .text(function(d) { return d.subtitle })
        .attr("x", function(d) { return d.x + ge_width/2; })
        .attr("y", function(d) { return d.y + ge_height/12 + + ge_height/6 + 5 });

    nodes
        .append("a")
        .attr("class", "launch-node-modal")
        .attr("data-toggle", "modal")
        .attr("data-target", "#myModal")
        .on("click", function(d) {
            var url = d.url;
            var title = d.title;
            $.ajax({
                type: "GET",
                url: url,
                success: function (data) {
                    $('.modal-body').html(data);
                    $('.modal-title').html(title);
                },
                error: function () {
                    alert('Error launching the modal')
                }
            })
        })
        .append("circle")
        .attr("class", "circle")
        .attr("r", circle_r)
        .attr("cx", function(d) { return (d.x + ge_width - circle_r - 10); })
        .attr("cy", function(d) { return (d.y + ge_height - circle_r - 10); });

    nodes
        .append("line")
        .attr("class", "line")
        .attr("x1", function(d) { return (d.x + ge_width - circle_r - 10 - circle_r + 3)})
        .attr("y1", function(d) { return (d.y + ge_height - circle_r - 10)})
        .attr("x2", function(d) { return (d.x + ge_width - circle_r - 10 + circle_r - 3)})
        .attr("y2", function(d) { return (d.y + ge_height - circle_r - 10)});

    nodes
        .append("line")
        .attr("class", "line")
        .attr("x1", function(d) { return (d.x + ge_width - circle_r - 10)})
        .attr("y1", function(d) { return (d.y + ge_height - circle_r - 10 - circle_r + 3)})
        .attr("x2", function(d) { return (d.x + ge_width - circle_r - 10)})
        .attr("y2", function(d) { return (d.y + ge_height - circle_r - 10 + circle_r - 3)});
});
