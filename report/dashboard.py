# dashboard.py
from fasthtml.common import *
import matplotlib.pyplot as plt

# -----------------------------
# Import employee_events modules
# -----------------------------
import sys
from pathlib import Path

# Add python-package/employee_events to sys.path
workspace_root = Path(__file__).parent.parent.resolve()
sys.path.insert(0, str(workspace_root / "python-package" / "employee_events"))

from employee import Employee
from team import Team
from query_base import QueryBase

# -----------------------------
# Import load_model function
# -----------------------------
sys.path.insert(0, str(workspace_root / "python-package"))
from utils import load_model

# -----------------------------
# Base and combined components
# -----------------------------
from base_components import Dropdown, BaseComponent, Radio, MatplotlibViz, DataTable
from combined_components import FormGroup, CombinedComponent

# -----------------------------
# Custom Components
# -----------------------------

# ReportDropdown
class ReportDropdown(Dropdown):

    def build_component(self, model, *args, **kwargs):
        self.label = getattr(model, 'name', '')
        return super().build_component(model, *args, **kwargs)

    def component_data(self, model, *args, **kwargs):
        return model.names()

# Header
class Header(BaseComponent):

    def build_component(self, model, *args, **kwargs):
        return H1(getattr(model, 'name', ''))

# LineChart
class LineChart(MatplotlibViz):

    def visualization(self, model, asset_id, *args, **kwargs):
        df = model.event_counts(asset_id).fillna(0).set_index('event_date').sort_index().cumsum()
        df.columns = ['Positive', 'Negative']
        fig, ax = plt.subplots()
        df.plot(ax=ax)
        self.set_axis_styling(ax, border_color='black', font_color='black')
        ax.set_title('Cumulative Events')
        ax.set_xlabel('Date')
        ax.set_ylabel('Event Count')

# BarChart
class BarChart(MatplotlibViz):

    predictor = load_model()

    def visualization(self, model, asset_id, *args, **kwargs):
        data = model.model_data(asset_id)
        pred_proba = self.predictor.predict_proba(data)[:, 1]

        if getattr(model, 'name', '').lower() == 'team':
            pred = pred_proba.mean()
        else:
            pred = pred_proba[0]

        fig, ax = plt.subplots()
        ax.barh([''], [pred])
        ax.set_xlim(0, 1)
        ax.set_title('Predicted Recruitment Risk', fontsize=20)
        self.set_axis_styling(ax, border_color='black', font_color='black')

# Visualizations container
class Visualizations(CombinedComponent):
    children = [LineChart(), BarChart()]
    outer_div_type = Div(cls='grid')

# NotesTable
class NotesTable(DataTable):

    def component_data(self, model, entity_id, *args, **kwargs):
        return model.notes(entity_id)

# DashboardFilters
class DashboardFilters(FormGroup):

    id = "top-filters"
    action = "/update_data"
    method = "POST"
    children = [
        Radio(
            values=["Employee", "Team"],
            name='profile_type',
            hx_get='/update_dropdown',
            hx_target='#selector'
        ),
        ReportDropdown(
            id="selector",
            name="user-selection"
        )
    ]

# Main Report
class Report(CombinedComponent):
    children = [
        Header(),
        DashboardFilters(),
        Visualizations(),
        NotesTable()
    ]

# -----------------------------
# Initialize fasthtml app
# -----------------------------
app = App()
report = Report()

# -----------------------------
# Routes
# -----------------------------

@app.get('/')
def root(r):
    return report(1, Employee())

@app.get('/employee/{id}')
def employee_page(r, id: str):
    return report(int(id), Employee())

@app.get('/team/{id}')
def team_page(r, id: str):
    return report(int(id), Team())

# Keep the Udacity-provided update routes
@app.get('/update_dropdown{r}')
def update_dropdown(r):
    dropdown = DashboardFilters.children[1]
    print('PARAM', r.query_params['profile_type'])
    if r.query_params['profile_type'] == 'Team':
        return dropdown(None, Team())
    elif r.query_params['profile_type'] == 'Employee':
        return dropdown(None, Employee())

@app.post('/update_data')
async def update_data(r):
    from fasthtml.common import RedirectResponse
    data = await r.form()
    profile_type = data._dict['profile_type']
    id = data._dict['user-selection']
    if profile_type == 'Employee':
        return RedirectResponse(f"/employee/{id}", status_code=303)
    elif profile_type == 'Team':
        return RedirectResponse(f"/team/{id}", status_code=303)

# -----------------------------
# Start the dashboard
# -----------------------------
serve()
