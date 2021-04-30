package example

/**
 * 该文件是有工具生成，请不要直接修改这个文件
 * 
 */

class ServerError {
    companion object {
        {% for item in errorcodes %}
            {% if item.is_comment() %}
            //===== {{item.comment}}

            {% else %}
                {% if item.comment %}
            // {{item.comment}}
                {% endif %}
            const val {{item.name}}:Long = {{item.code}}

            {% endif %}
        {% endfor %}
    }
}
