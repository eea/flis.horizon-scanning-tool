d3.json("relations", function(error, graph) {
    var width = $("#svg-relations").width();
    var height = (width + graph.nodes.length * 200) / 2.2;
    var svg = d3.select("#svg-relations")
      .append("svg")
      .attr("width", width)
      .attr("height", height);
    var charge = width * -100 / graph.nodes.length;
    var distance = width / 20 + 100;
    var ge_width = width / 30  + 100;
    var ge_height = width / 20 + 100;

    var max_title_size = width / 500 + 16;
    var max_fig_size = width / 500 + 18;
    var title_font_size = "13px";

    var circle_r = ge_width / 18;

    var force = d3.layout.force()
        .charge(charge)
        .linkDistance(distance)
        .size([width, height])
        .nodes(graph.nodes)
        .links(graph.links)
        .start();

    for (var i=0; i<1000; i++) {
        force.tick();
    }
    force.stop();

    function node_x(point){ return point.x - ge_width/2 }
    function node_y(point){ return point.y - ge_height/2 }
    function link_cx(point){ return (point.source.x + point.target.x)/2 }
    function link_cy(point, offset){ return (point.source.y + point.target.y)/2 + offset }

    //Draw relation
    var links = svg.selectAll()
        .data(graph.links).enter();

    var defs = svg.append("defs");

    defs.append("marker")
      .attr("id", "arrowhead-end")
      .attr("refX", 10)
      .attr("refY", 5)
      .attr("markerWidth", 10)
      .attr("markerHeight", 10)
      .attr("orient", "auto")
      .append("path")
          .attr("d", "M 0 0 L 10 5 L 0 10 z");

    defs.append("marker")
      .attr("id", "arrowhead-start")
      .attr("refX", -2)
      .attr("refY", 5)
      .attr("markerWidth", 10)
      .attr("markerHeight", 10)
      .attr("orient", "auto")
      .append("path")
          .attr("d", "M -2 5 L 8 0 L 8 10 z");

    var links_connections = links.append("line")
        .attr("class", "link")
        .attr("marker-end", "url(#arrowhead-end)")
        .attr("x1", function(d) { return find_x(d.source.x, d.source.y, d.target.x, d.target.y, ge_width, ge_height) })
        .attr("y1", function(d) { return find_y(d.source.x, d.source.y, d.target.x, d.target.y, ge_width, ge_height) })
        .attr("x2", function(d) { return find_x(d.target.x, d.target.y, d.source.x, d.source.y, ge_width, ge_height) })
        .attr("y2", function(d) { return find_y(d.target.x, d.target.y, d.source.x, d.source.y, ge_width, ge_height) })
        .each(function(link) {
            if (link.type == 2)
                d3.select(this).attr("marker-start", "url(#arrowhead-start)");
        });

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

    var insertFigures = function (d) {
        var el = d3.select(this);
        if (d.figures.length > 0) {
            d.figures.slice(0, 4).forEach( function(figure) {
                if (figure.length > max_fig_size)
                  figure = figure.substring(0, max_fig_size - 1) + ' ...'

                el
                .append("tspan")
                .attr("dy", 20)
                .attr("x", node_x(d) + 5)
                .text("• " + figure);
            });
        }
        else {
            el
            .append("tspan")
            .attr("dy", 20)
            .attr("dx", -100)
            .style("font-style", "italic")
            .text("No facts and figures.");
        }
    }

    var nodes_figures = nodes
        .append("text")
        .text("Facts and figures: ")
        .style("font-size", title_font_size)
        .attr("x", function(d) { return node_x(d) + 5 })
        .attr("y", function(d) { return node_y(d) + ge_height/12 + ge_height/3 })
        .each(insertFigures);

    var title_tooltip = false;
    var nodes_title = nodes
        .append("text")
        .attr("class", "d3-node-title")
        .text(function(d) {
            if (d.title.length > max_title_size) {
                title_tooltip = true;
                return d.title.substring(0, max_title_size-1) + ' ...'
            }
            return d.title;
        })
        .style("font-size", title_font_size)
        .attr("x", function(d) { return node_x(d) + ge_width/2 })
        .attr("y", function(d) { return node_y(d) + ge_height/12 + 5 });
    nodes_title
        .append("svg:title")
        .text(function(d) {
            if(d.title.length > 10){
                return d.title;
            }
            return '';
        });

    if(title_tooltip==true) {
        nodes_title
            .append("p")
            .attr("svg:title", function (d) {
                if (d.title.length > 10) {
                    return d.title;
                }
                return '';
            });
    }

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

    var nodes_subtitle = nodes
        .append("text")
        .attr("class", "d3-node-subtitle")
        .text(function(d) { return d.subtitle })
        .attr("x", function(d) { return node_x(d) + ge_width/2; })
        .attr("y", function(d) { return node_y(d) + ge_height/12 + ge_height/6 + 5 });

    var plus = nodes
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

    function dragmove(d) {
        d.x += d3.event.dx;
        d.y += d3.event.dy;
        links_connections
            .attr("x1", function(d) { return find_x(d.source.x, d.source.y, d.target.x, d.target.y, ge_width, ge_height) })
            .attr("y1", function(d) { return find_y(d.source.x, d.source.y, d.target.x, d.target.y, ge_width, ge_height) })
            .attr("x2", function(d) { return find_x(d.target.x, d.target.y, d.source.x, d.source.y, ge_width, ge_height) })
            .attr("y2", function(d) { return find_y(d.target.x, d.target.y, d.source.x, d.source.y, ge_width, ge_height) });
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

        svg.selectAll("tspan").remove();
        nodes_figures
            .attr("x", function(d) { return node_x(d) + 5 })
            .attr("y", function(d) { return node_y(d) + ge_height/12 + ge_height/3 })
            .each(insertFigures);
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
});

function find_x(x, y, a, b, w, h) {
    var tga = Math.abs(a-x)/Math.abs(b-y);
    var tgb = w/h;
    if(tga<tgb){
        var coef = (h/2) * Math.abs(a-x)/Math.abs(b-y);
        if(a>x){
            return x + coef;
        }
        return x - coef;
    }
    else{
        if(a>x){
            return x + w/2;
        }
        return x-w/2;
    }
}

function find_y(x, y, a, b, w, h) {
    var tga = Math.abs(a-x)/Math.abs(b-y);
    var tgb = w/h;
    if(tga<tgb) {
        if (b > y) {
            return y + h/2;
        }
        return y - h/2;
    }
    else{
        var coef = (w/2) * Math.abs(b-y)/Math.abs(a-x);
        if (b>y){
            return y+coef;
        }
        return y-coef;
    }
}
