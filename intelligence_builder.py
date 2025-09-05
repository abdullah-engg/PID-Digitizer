from pyvis.network import Network
import os

def build_knowledge_graph_from_tables(data):
    """
    Builds an interactive knowledge graph from the category-based AI data,
    using a clean hierarchical layout.
    """
    net = Network(height="800px", width="100%", bgcolor="#f0f2f6", font_color="black", notebook=True, cdn_resources='in_line', directed=True)
    
   
    net.set_options("""
    var options = {
      "layout": {
        "hierarchical": {
          "enabled": true,
          "direction": "UD", 
          "sortMethod": "directed"
        }
      },
      "physics": {
        "enabled": true,
        "hierarchicalRepulsion": {
          "centralGravity": 0.0,
          "springLength": 150,
          "springConstant": 0.01,
          "nodeDistance": 150,
          "damping": 0.09
        },
        "minVelocity": 0.75,
        "solver": "hierarchicalRepulsion"
      }
    }
    """)

  
    category_properties = {
        "Equipment": {"color": "#3498db", "shape": "box", "size": 30},
        "Instrumentation": {"color": "#f1c40f", "shape": "ellipse", "size": 20},
        "Valves": {"color": "#2ecc71", "shape": "triangle", "size": 15},
    }

    def add_nodes_from_category(category_name, category_key):
        if category_key in data and data[category_key]:
            props = category_properties.get(category_name, {"color": "#95a5a6", "shape": "dot"})
            for item in data[category_key]:
                tag = item.get('tag')
                if tag and tag not in net.get_nodes():
                    title = f"<b>Tag:</b> {tag}<br><b>Category:</b> {category_name}<br>"
                    for key, value in item.items():
                        if key not in ['tag', 'bounding_box']:
                            title += f"<b>{key.replace('_', ' ').capitalize()}:</b> {value}<br>"
                    net.add_node(tag, label=tag, title=title, **props)
    
    add_nodes_from_category("Equipment", "equipment")
    add_nodes_from_category("Instrumentation", "instrumentation")
    add_nodes_from_category("Valves", "valves")
    

    if "lines" in data and data["lines"]:
        all_nodes = net.get_nodes()
        for line in data["lines"]:
            source = line.get('source_tag')
            dest = line.get('destination_tag')
            if source and dest:
                if source in all_nodes and dest in all_nodes:
                    net.add_edge(source, dest, title=line.get('line_number_tag', ''))
    

    output_dir = "temp_uploads"
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "pid_knowledge_graph.html")
    
    html_content = net.generate_html()
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
        
    return output_path

