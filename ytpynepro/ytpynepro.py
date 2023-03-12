import  pynecone as pc
from .models import User
import string
import pandas as pd

class MyState(pc.State):
    name:str
    age:int
    show_dialog:bool = False

    alluser = []
    list_user = alluser.copy()


    def addtotable(self):
        # NOW ADD DATA TO TABLE SQLITE 
        # BY DEFAULT PYNECONE SET DEFAULT DB IS pynecone.db

        with pc.session() as s:
            s.add(
                User(
                    name=self.name,
                    age=self.age
                    )

                )
            s.commit()

        # AND IF YOU SUCCESS ADD TO TABLE
        # THE SHOW DIALOG SUCCESS
        self.show_dialog = True



    def refreshtable(self):
        # AND NOW REFRESH TABLE IF YOU ADD EDIT DELETE
        # THE TABLE
        # AND CHANGE RESULT TABLE

        with pc.session() as s:
            self.alluser = s.query(User).all()
            # AND CONVERT TO DICT
            # ARRAY JSON
            # FROM RESULT TABLE SQLITE
            self.alluser = [{"name":u.name,"age":u.age} for u in self.alluser]

        print(self.alluser)

    @pc.var
    def result_data(self):
        # AND FROM JSON self.alluser CONVERT TO DATAFRAME
        # WITH PANDAS
        # THE DATATABLE WORK WITH DATAFRAME
        return pd.DataFrame(
            self.alluser,
            # AND SELECTED COLUMN YOU WANT
            columns=["name","age"]

            )
        


    def change_dialog(self):
        # AND SHOW IF SUCCESS AND HIDE IF YOU CLICK CLOSE
        self.show_dialog = not(self.show_dialog)


def index():
    return pc.vstack(

        # AND NOW CREATE ALERT DIALOG WIDGET
        pc.alert_dialog(
            pc.alert_dialog_overlay(
                pc.alert_dialog_content(
                    pc.alert_dialog_header("success"),
                    pc.alert_dialog_body(
                        "YOU SUCCES ADD"
                        ),
                    pc.alert_dialog_footer(
                        pc.button(
                            "close now",
                            on_click=MyState.change_dialog
                            )
                        )

                    )

                ),
            is_open = MyState.show_dialog

            ),







        pc.hstack(
        pc.text("name"),
        pc.input(on_change=MyState.set_name)
            ),

        pc.hstack(
        pc.text("age"),
        pc.input(on_change=MyState.set_age)
            ),
        pc.button("add to table",
            on_click=MyState.addtotable
            ),
         pc.button("refresh table",
            on_click=MyState.refreshtable
            ),

         # AND NOW CREATE DATATABLE
         # AND READ FROM JSON 
         pc.data_table(
            data=MyState.result_data,
            pagination=True,
            sort=True,
            search=True,


            )


        )

app = pc.App(state=MyState)
app.add_page(index)
app.compile()
