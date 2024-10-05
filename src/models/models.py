from __future__ import annotations
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped

from src.db.base import Base
from src.models.BuyIngreds import BuyIngreds
from src.models.ToweekRecipes import ToweekRecipes

class User(Base):
    __tablename__ = 'm_user'

    user_id = Column(Integer, primary_key=True, nullable=False)
    user_nm = Column(String, nullable=False)
    mail_addr = Column(String, nullable=False)
    password = Column(String, nullable=False)
    crt_at = Column(String, nullable=True)
    upd_at = Column(String, nullable=True)
    crt_by = Column(String, nullable=True)
    upd_by = Column(String, nullable=True)
    version = Column(Integer, nullable=True)

    rel_m_user_config: Mapped[list[UserConfig]] = relationship("UserConfig", back_populates="rel_m_user")
    rel_t_user_group_rel: Mapped[list[UserGroupRel]] = relationship("UserGroupRel", back_populates="rel_m_user")
    rel_m_group: Mapped[list[Group]] = relationship("Group", back_populates="rel_m_user")
    rel_t_recipe: Mapped[list[Recipe]] = relationship("Recipe", back_populates="rel_m_user")
    rel_t_menu_plan: Mapped[list[MenuPlan]] = relationship("MenuPlan", back_populates="rel_m_user")
    rel_m_ingred: Mapped[list[Ingred]] = relationship("Ingred", back_populates="rel_m_user")
    rel_m_ingred_unit_conv: Mapped[list[IngredUnitConv]] = relationship("IngredUnitConv", back_populates="rel_m_user")
    rel_w_buy_ingreds: Mapped[list[BuyIngreds]] = relationship("BuyIngreds", back_populates="rel_m_user")
    rel_w_toweek_recipes: Mapped[list[ToweekRecipes]] = relationship("ToweekRecipes", back_populates="rel_m_user")


class UserConfig(Base):
    __tablename__ = 'm_user_config'

    user_config_id = Column(Integer, primary_key=True, nullable=False)
    user_id = Column(Integer, ForeignKey('m_user.user_id'), nullable=False)
    config_type = Column(String, nullable=False)
    config_val = Column(String, nullable=True)
    crt_at = Column(String, nullable=True)
    upd_at = Column(String, nullable=True)
    crt_by = Column(String, nullable=True)
    upd_by = Column(String, nullable=True)
    version = Column(Integer, nullable=True)

    rel_m_user: Mapped[User] = relationship("User", back_populates="rel_m_user_config")


class Recipe(Base):
    __tablename__ = 't_recipe'

    recipe_id = Column(Integer, primary_key=True, nullable=False)
    recipe_nm = Column(String, nullable=False)
    recipe_type = Column(String, nullable=True)
    owner_id = Column(String, ForeignKey('m_user.user_id'), nullable=False)
    recipe_url = Column(String, nullable=True)
    visibility_flg = Column(String, nullable=True)
    crt_at = Column(String, nullable=True)
    upd_at = Column(String, nullable=True)
    crt_by = Column(String, nullable=True)
    upd_by = Column(String, nullable=True)
    version = Column(Integer, nullable=True)
    recipe_nm_k = Column(String, nullable=True)

    rel_m_user: Mapped[User] = relationship("User", back_populates="rel_t_recipe")
    rel_t_recipe_ingred: Mapped[list[RecipeIngred]] = relationship("RecipeIngred", back_populates="rel_t_recipe")
    rel_t_menu_plan_det: Mapped[list[MenuPlanDet]] = relationship("MenuPlanDet", back_populates="rel_t_recipe")
    rel_w_toweek_recipes: Mapped[list[ToweekRecipes]] = relationship("ToweekRecipes", back_populates="rel_t_recipe")

class RecipeIngred(Base):
    __tablename__ = 't_recipe_ingred'

    recipe_ingred_id = Column(Integer, primary_key=True, nullable=False)
    recipe_id = Column(Integer, ForeignKey('t_recipe.recipe_id'), nullable=False)
    ingred_id = Column(Integer, ForeignKey('m_ingred.ingred_id'), nullable=False)
    qty = Column(Float, nullable=False)
    unit_cd = Column(String, nullable=False)
    crt_at = Column(String, nullable=True)
    upd_at = Column(String, nullable=True)
    crt_by = Column(String, nullable=True)
    upd_by = Column(String, nullable=True)
    version = Column(Integer, nullable=True)

    rel_t_recipe: Mapped[Recipe] = relationship("Recipe", back_populates="rel_t_recipe_ingred")
    rel_m_ingred: Mapped[Ingred] = relationship("Ingred", back_populates="rel_t_recipe_ingred")


class Group(Base):
    __tablename__ = 'm_group'

    group_id = Column(Integer, primary_key=True, nullable=False)
    group_nm = Column(String, nullable=False)
    owner_user_id = Column(Integer, ForeignKey('m_user.user_id'), nullable=False)
    crt_at = Column(String, nullable=True)
    upd_at = Column(String, nullable=True)
    crt_by = Column(String, nullable=True)
    upd_by = Column(String, nullable=True)
    version = Column(Integer, nullable=True)

    rel_t_user_group_rel: Mapped[list[UserGroupRel]] = relationship("UserGroupRel", back_populates="rel_m_group")
    rel_m_user: Mapped[User] = relationship("User", back_populates="rel_m_group")


class UserGroupRel(Base):
    __tablename__ = 't_user_group_rel'

    user_group_rel_id = Column(Integer, primary_key=True, nullable=False)
    user_id = Column(Integer, ForeignKey('m_user.user_id'), nullable=False)
    group_id = Column(Integer, ForeignKey('m_group.group_id'), nullable=False)
    crt_at = Column(String, nullable=True)
    upd_at = Column(String, nullable=True)
    crt_by = Column(String, nullable=True)
    upd_by = Column(String, nullable=True)
    version = Column(Integer, nullable=True)

    rel_m_user: Mapped[User] = relationship("User", back_populates="rel_t_user_group_rel")
    rel_m_group: Mapped[Group] = relationship("Group", back_populates="rel_t_user_group_rel")


class Ingred(Base):
    __tablename__ = 'm_ingred'

    ingred_id = Column(Integer, primary_key=True, nullable=False)
    ingred_nm = Column(String, nullable=False)
    ingred_nm_k = Column(String, nullable=True)
    parent_ingred_nm = Column(String, nullable=False)
    standard_unit_cd = Column(String, nullable=False)
    sales_area_type = Column(String, nullable=True)
    owner_user_id = Column(Integer, ForeignKey('m_user.user_id'), nullable=False)
    crt_at = Column(String, nullable=True)
    upd_at = Column(String, nullable=True)
    crt_by = Column(String, nullable=True)
    upd_by = Column(String, nullable=True)
    version = Column(Integer, nullable=True)

    rel_m_ingred_unit_conv: Mapped[list[IngredUnitConv]] = relationship("IngredUnitConv", back_populates="rel_m_ingred")
    rel_m_user: Mapped[User] = relationship("User", back_populates="rel_m_ingred")
    rel_t_recipe_ingred: Mapped[list[RecipeIngred]] = relationship("RecipeIngred", back_populates="rel_m_ingred")
    # rel_w_buy_ingreds: Mapped[list[BuyIngreds]] = relationship("BuyIngreds", back_populates="rel_m_ingred")
    

class IngredUnitConv(Base):
    __tablename__ = 'm_ingred_unit_conv'

    ingred_unit_conv_id = Column(Integer, primary_key=True, nullable=False)
    ingred_id = Column(Integer, ForeignKey('m_ingred.ingred_id'), nullable=False)
    from_unit_cd = Column(String, nullable=False)
    conv_rate = Column(Float, nullable=False)
    owner_user_id = Column(Integer, ForeignKey('m_user.user_id'), nullable=False)
    crt_at = Column(String, nullable=True)
    upd_at = Column(String, nullable=True)
    crt_by = Column(String, nullable=True)
    upd_by = Column(String, nullable=True)
    version = Column(Integer, nullable=True)

    rel_m_ingred: Mapped[Ingred] = relationship("Ingred", back_populates="rel_m_ingred_unit_conv")
    rel_m_user: Mapped[User] = relationship("User", back_populates="rel_m_ingred_unit_conv")


class MenuPlan(Base):
    __tablename__ = 't_menu_plan'

    menu_plan_id = Column(Integer, primary_key=True, nullable=False)
    menu_plan_nm = Column(String, nullable=False)
    menu_plan_nm_k = Column(String, nullable=True)
    owner_user_id = Column(Integer, ForeignKey('m_user.user_id'), nullable=False)
    visibility_flg = Column(String, nullable=True)
    crt_at = Column(String, nullable=True)
    upd_at = Column(String, nullable=True)
    crt_by = Column(String, nullable=True)
    upd_by = Column(String, nullable=True)
    version = Column(Integer, nullable=True)

    rel_m_user: Mapped[User] = relationship("User", back_populates="rel_t_menu_plan")
    rel_t_menu_plan_det: Mapped[list[MenuPlanDet]] = relationship("MenuPlanDet", back_populates="rel_t_menu_plan")


class MenuPlanDet(Base):
    __tablename__ = 't_menu_plan_det'

    menu_plan_det_id = Column(Integer, primary_key=True, nullable=False)
    menu_plan_id = Column(Integer, ForeignKey('t_menu_plan.menu_plan_id'), nullable=False)
    week_day_cd = Column(String, nullable=False)
    recipe_id = Column(Integer, ForeignKey('t_recipe.recipe_id'), nullable=True)
    crt_at = Column(String, nullable=True)
    upd_at = Column(String, nullable=True)
    crt_by = Column(String, nullable=True)
    upd_by = Column(String, nullable=True)
    version = Column(Integer, nullable=True)

    rel_t_menu_plan: Mapped[MenuPlan] = relationship("MenuPlan", back_populates="rel_t_menu_plan_det")
    rel_t_recipe: Mapped[Recipe] = relationship("Recipe", back_populates="rel_t_menu_plan_det")


class AppConst(Base):
    __tablename__ = 'c_app_const'

    const_id = Column(Integer, primary_key=True, nullable=False)
    type_cd = Column(String, nullable=False)
    type_nm = Column(String, nullable=True)
    val = Column(String, nullable=True)
    val_content = Column(String, nullable=True)
    sort_seq = Column(Integer, nullable=True)
    generic_item1 = Column(String, nullable=True)
    generic_item2 = Column(String, nullable=True)
    crt_at = Column(String, nullable=True)
    upd_at = Column(String, nullable=True)
    crt_by = Column(String, nullable=True)
    upd_by = Column(String, nullable=True)
    version = Column(Integer, nullable=True)

