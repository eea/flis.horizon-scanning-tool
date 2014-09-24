var width = $("#svg-relations").width();
var height = width;

var svg = d3.select("#svg-relations").append("svg")
    .attr("width", width)
    .attr("height", height);

d3.json("relations", function(error, graph) {

    var ge_width, ge_height, title_font_size, charge;
    if(width<750) {
        charge = -2500;
        title_font_size = "9px";
        ge_width = width/8;
        ge_height = height/6;
    }
    else if(width<900) {
        charge = -4000;
        title_font_size = "9px";
        ge_width = width/8;
        ge_height = height/6;
    }
    else if(width<1100) {
        charge = -6000;
        title_font_size = "10px";
        ge_width = width/8;
        ge_height = height/7;
    }
    else {
        charge = -8000;
        title_font_size = "10px";
        ge_width=width/10;
        ge_height=height/10;
    }
    var circle_r = ge_width/18;

    var force = d3.layout.force()
        .charge(charge)
        .linkDistance(100)
        .size([width, height])
        .nodes(graph.nodes)
        .links(graph.links)
        .start();

    for(var i=0;i<300;i++){
        force.tick();
    }
    force.stop();

    //Draw relation
    var links = svg.selectAll()
        .data(graph.links).enter();

    var links_connections = links.append("line")
        .attr("class", "link")
        .attr("x1", function(d) { return d.source.x })
        .attr("y1", function(d) { return d.source.y })
        .attr("x2", function(d) { return d.target.x })
        .attr("y2", function(d) { return d.target.y });

    function node_x(point){ return point.x - ge_width/2 }
    function node_y(point){ return point.y - ge_height/2 }
    function link_cx(point){ return (point.source.x + point.target.x)/2 }
    function link_cy(point, offset){ return (point.source.y + point.target.y)/2 + offset }

    var links_ellipse = links.append("ellipse")
        .attr("class", "ellipse")
        .attr("rx", 3*circle_r)
        .attr("ry", 3*circle_r)
        .attr("cx", function(d) { return link_cx(d) })
        .attr("cy", function(d) { return link_cy(d, 0) });

    var plus = svg.selectAll()
        .data(graph.links).enter()
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
                    $('.modal-title').html('Relation');
                },
                error: function () {
                    alert('Error launching the modal')
                }
            })
        });

    var links_plus_circle = plus.append("circle")
        .attr("class", "circle")
        .attr("r", circle_r)
        .attr("cx", function(d) { return link_cx(d) })
        .attr("cy", function(d) { return link_cy(d, 2*circle_r) });

    var links_plus_line1 = plus.append("line")
        .attr("class", "line")
        .attr("x1", function(d) { return link_cx(d) - circle_r + 2 })
        .attr("y1", function(d) { return link_cy(d, 2*circle_r) })
        .attr("x2", function(d) { return link_cx(d) + circle_r - 2 })
        .attr("y2", function(d) { return link_cy(d, 2*circle_r) });

    var links_plus_line2 = plus.append("line")
        .attr("class", "line")
        .attr("x1", function(d) { return link_cx(d) })
        .attr("y1", function(d) { return link_cy(d, 2*circle_r) - circle_r + 2 })
        .attr("x2", function(d) { return link_cx(d) })
        .attr("y2", function(d) { return link_cy(d, 2*circle_r) + circle_r - 2 });

    //Draw Generic Element
    var node_drag = d3.behavior.drag()
        .on("drag", dragmove);

    function dragmove(d) {
        d.x += d3.event.dx;
        d.y += d3.event.dy;
        links_connections
            .attr("x1", function(d) { return d.source.x })
            .attr("y1", function(d) { return d.source.y })
            .attr("x2", function(d) { return d.target.x })
            .attr("y2", function(d) { return d.target.y });
        links_ellipse
            .attr("cx", function(d) { return link_cx(d) })
            .attr("cy", function(d) { return link_cy(d, 0) });
        links_plus_circle
            .attr("cx", function(d) { return link_cx(d) })
            .attr("cy", function(d) { return link_cy(d, 2*circle_r) });
        links_plus_line1
            .attr("x1", function(d) { return link_cx(d) - circle_r + 2 })
            .attr("y1", function(d) { return link_cy(d, 2*circle_r) })
            .attr("x2", function(d) { return link_cx(d) + circle_r - 2 })
            .attr("y2", function(d) { return link_cy(d, 2*circle_r) });
        links_plus_line2
            .attr("x1", function(d) { return link_cx(d) })
            .attr("y1", function(d) { return link_cy(d, 2*circle_r) - circle_r + 2 })
            .attr("x2", function(d) { return link_cx(d) })
            .attr("y2", function(d) { return link_cy(d, 2*circle_r) + circle_r - 2 });

        nodes_rect
            .attr("x", function(d) { return node_x(d) })
            .attr("y", function(d) { return node_y(d) });
        nodes_title
            .attr("x", function(d) { return node_x(d) + ge_width/2 })
            .attr("y", function(d) { return node_y(d) + ge_height/12 + 5 });
        nodes_subtitle_rect
            .attr("x", function(d) { return node_x(d) })
            .attr("y", function(d) { return node_y(d) + ge_height/6 });
        nodes_subtitle
            .attr("x", function(d) { return node_x(d) + ge_width/2 })
            .attr("y", function(d) { return node_y(d) + ge_height/12 + + ge_height/6 + 5 });
        nodes_plus_circle
            .attr("cx", function(d) { return node_x(d) + ge_width - circle_r - 2 })
            .attr("cy", function(d) { return node_y(d) + ge_height - circle_r - 2 });
        nodes_plus_line1
            .attr("x1", function(d) { return node_x(d) + ge_width - circle_r - 2 - circle_r + 2 })
            .attr("y1", function(d) { return node_y(d) + ge_height - circle_r - 2 })
            .attr("x2", function(d) { return node_x(d) + ge_width - circle_r - 2 + circle_r - 2 })
            .attr("y2", function(d) { return node_y(d) + ge_height - circle_r - 2 });
        nodes_plus_line2
            .attr("x1", function(d) { return node_x(d) + ge_width - circle_r - 2 })
            .attr("y1", function(d) { return node_y(d) + ge_height - circle_r - 2 - circle_r + 2 })
            .attr("x2", function(d) { return node_x(d) + ge_width - circle_r - 2 })
            .attr("y2", function(d) { return node_y(d) + ge_height - circle_r - 2 + circle_r - 2 });
    }

    var nodes = svg.selectAll()
        .data(graph.nodes).enter().append("svg:g")
        .call(node_drag);

    var nodes_rect = nodes
        .append("rect")
        .attr("class", "node")
        .attr("width", ge_width)
        .attr("height", ge_height)
        .attr("x", function(d) { return node_x(d) })
        .attr("y", function(d) { return node_y(d) });

    var nodes_title = nodes
        .append("text")
        .attr("class", "d3-node-title")
        .text(function(d) { return d.title })
        .style("font-size", title_font_size)
        .attr("x", function(d) { return node_x(d) + ge_width/2 })
        .attr("y", function(d) { return node_y(d) + ge_height/12 + 5 });

    var nodes_subtitle_rect = nodes
        .append("rect")
        .attr("class", function(d) { switch (d.subtitle_color) {
                case 0: return "d3-box-salmon";
                case 1: return "d3-box-purple";
                case 2: return "d3-box-pink";

        }})
        .attr("width", ge_width)
        .attr("height", ge_height/6)
        .attr("x", function(d) { return node_x(d) })
        .attr("y", function(d) { return node_y(d) + ge_height/6 });

//    var ul = nodes_subtitle_rect.append("ul").selectAll("li").data(graph.nodes).enter();
//    ul.append("li").text('ceva 1');
//    ul.append("li").text('ceva 2');

    var nodes_subtitle = nodes
        .append("text")
        .attr("class", "d3-node-subtitle")
        .text(function(d) { return d.subtitle })
        .attr("x", function(d) { return node_x(d) + ge_width/2; })
        .attr("y", function(d) { return node_y(d) + ge_height/12 + + ge_height/6 + 5 });

    plus = nodes
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
        });

    var nodes_plus_circle = plus.append("circle")
        .attr("class", "circle")
        .attr("r", circle_r)
        .attr("cx", function(d) { return node_x(d) + ge_width - circle_r - 2 })
        .attr("cy", function(d) { return node_y(d) + ge_height - circle_r - 2 });

    var nodes_plus_line1 = plus.append("line")
        .attr("class", "line")
        .attr("x1", function(d) { return node_x(d) + ge_width - circle_r - 2 - circle_r + 2 })
        .attr("y1", function(d) { return node_y(d) + ge_height - circle_r - 2 })
        .attr("x2", function(d) { return node_x(d) + ge_width - circle_r - 2 + circle_r - 2 })
        .attr("y2", function(d) { return node_y(d) + ge_height - circle_r - 2 });

    var nodes_plus_line2 = plus.append("line")
        .attr("class", "line")
        .attr("x1", function(d) { return node_x(d) + ge_width - circle_r - 2 })
        .attr("y1", function(d) { return node_y(d) + ge_height - circle_r - 2 - circle_r + 2 })
        .attr("x2", function(d) { return node_x(d) + ge_width - circle_r - 2 })
        .attr("y2", function(d) { return node_y(d) + ge_height - circle_r - 2 + circle_r - 2 });
});
