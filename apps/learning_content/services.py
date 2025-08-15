# apps/learning_content/services.py

from .models import Material, MaterialNode

def duplicate_material(template_material: Material, user) -> Material:
    """
    共有テンプレート教材を複製してユーザー専用教材を作成する。

    Args:
        template_material (Material): 複製元の公式テンプレート教材
        user: 複製後の教材の所有者（Userオブジェクト）

    Returns:
        Material: 複製されたユーザー専用教材オブジェクト

    処理内容:
        1. Materialを複製してownerを設定し、parent_templateに元教材を保持
        2. 元教材に紐づくMaterialNodeをすべて複製し、新しいMaterialに紐づける
           - parentは一旦Noneに設定（階層構造のコピーが必要な場合は再帰的処理が必要）
    """

    # Materialを複製
    new_material = Material.objects.create(
        title=template_material.title,
        description=template_material.description,
        owner=user,
        is_template=False,
        parent_template=template_material
    )

    # MaterialNodeを複製
    for node in template_material.nodes.all():
        MaterialNode.objects.create(
            material=new_material,
            title=node.title,
            description=node.description,
            parent=None,  # 階層構造もコピーする場合は再帰的に設定
            owner=user
        )

    return new_material
